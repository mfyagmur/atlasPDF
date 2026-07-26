import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pikepdf

from app.tools.compress.exceptions import InvalidPDFError

CompressionLevel = Literal["low", "recommended", "extreme"]

GHOSTSCRIPT_PDFSETTINGS: dict[CompressionLevel, str] = {
    "low": "/printer",
    "recommended": "/ebook",
    "extreme": "/screen",
}

GHOSTSCRIPT_CANDIDATES = ["gswin64c", "gswin32c", "gs"]


@dataclass
class CompressResult:
    output_path: Path
    original_size: int
    compressed_size: int
    savings_percent: float


def find_ghostscript() -> str | None:
    for candidate in GHOSTSCRIPT_CANDIDATES:
        if shutil.which(candidate):
            return candidate
    return None


def _compress_with_ghostscript(gs_bin: str, input_path: Path, output_path: Path, level: CompressionLevel) -> None:
    result = subprocess.run(
        [
            gs_bin,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={GHOSTSCRIPT_PDFSETTINGS[level]}",
            "-dNOPAUSE",
            "-dBATCH",
            "-dQUIET",
            f"-sOutputFile={output_path}",
            str(input_path),
        ],
        capture_output=True,
        timeout=120,
    )
    if result.returncode != 0 or not output_path.exists():
        raise RuntimeError(f"Ghostscript sıkıştırma başarısız: {result.stderr.decode(errors='ignore')}")


def _compress_with_pikepdf(input_path: Path, output_path: Path) -> None:
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(output_path, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
    except pikepdf.PasswordError as exc:
        raise InvalidPDFError(f"Şifreli PDF dosyası desteklenmiyor: {input_path.name}") from exc
    except pikepdf.PdfError as exc:
        raise InvalidPDFError(f"Bozuk PDF dosyası: {input_path.name}") from exc


def compress_pdf(input_path: Path, output_path: Path, level: CompressionLevel) -> CompressResult:
    original_size = input_path.stat().st_size

    gs_bin = find_ghostscript()
    if gs_bin is not None:
        try:
            _compress_with_ghostscript(gs_bin, input_path, output_path, level)
        except (RuntimeError, OSError, subprocess.SubprocessError):
            _compress_with_pikepdf(input_path, output_path)
    else:
        _compress_with_pikepdf(input_path, output_path)

    compressed_size = output_path.stat().st_size
    savings_percent = max(round((1 - compressed_size / original_size) * 100, 1), 0.0) if original_size else 0.0

    return CompressResult(
        output_path=output_path,
        original_size=original_size,
        compressed_size=compressed_size,
        savings_percent=savings_percent,
    )
