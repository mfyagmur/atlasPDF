from dataclasses import dataclass
from pathlib import Path

from pdf2docx import Converter
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.tools.pdf_to_word.exceptions import InvalidPDFError

SCANNED_CHARS_PER_PAGE_THRESHOLD = 20
SCANNED_WARNING = "Bu PDF taranmış görünüyor, sonuç düşük kaliteli olabilir."


@dataclass
class WordResult:
    output_path: Path
    warning: str | None


def _read_pdf(input_path: Path) -> PdfReader:
    try:
        reader = PdfReader(input_path)
    except PdfReadError as exc:
        raise InvalidPDFError(f"Bozuk PDF dosyası: {input_path.name}") from exc

    if reader.is_encrypted:
        raise InvalidPDFError(f"Şifreli PDF dosyası desteklenmiyor: {input_path.name}")

    return reader


def _looks_scanned(reader: PdfReader) -> bool:
    if not reader.pages:
        return False

    total_chars = sum(len((page.extract_text() or "").strip()) for page in reader.pages)
    avg_chars_per_page = total_chars / len(reader.pages)
    return avg_chars_per_page < SCANNED_CHARS_PER_PAGE_THRESHOLD


def pdf_to_word(input_path: Path, output_path: Path) -> WordResult:
    reader = _read_pdf(input_path)
    warning = SCANNED_WARNING if _looks_scanned(reader) else None

    try:
        converter = Converter(str(input_path))
        try:
            converter.convert(str(output_path))
        finally:
            converter.close()
    except Exception as exc:
        raise InvalidPDFError(f"PDF Word'e dönüştürülemedi: {input_path.name}") from exc

    return WordResult(output_path=output_path, warning=warning)
