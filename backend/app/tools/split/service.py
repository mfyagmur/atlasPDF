import re
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from app.tools.split.exceptions import InvalidPageRangeError, InvalidPDFError

RANGE_PATTERN = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")


def _read_pdf(input_path: Path) -> PdfReader:
    try:
        reader = PdfReader(input_path)
    except PdfReadError as exc:
        raise InvalidPDFError(f"Bozuk PDF dosyası: {input_path.name}") from exc

    if reader.is_encrypted:
        raise InvalidPDFError(f"Şifreli PDF dosyası desteklenmiyor: {input_path.name}")

    return reader


def get_page_count(input_path: Path) -> int:
    reader = _read_pdf(input_path)
    return len(reader.pages)


def parse_ranges(ranges_str: str, page_count: int) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []

    for part in ranges_str.split(","):
        match = RANGE_PATTERN.match(part)
        if not match:
            raise InvalidPageRangeError(f"Geçersiz aralık formatı: '{part.strip()}'")

        start, end = int(match.group(1)), int(match.group(2))
        if start < 1 or end < start:
            raise InvalidPageRangeError(f"Geçersiz aralık: '{part.strip()}'")
        if end > page_count:
            raise InvalidPageRangeError(
                f"Aralık, PDF'in toplam sayfa sayısını ({page_count}) aşıyor: '{part.strip()}'"
            )

        ranges.append((start, end))

    return ranges


def split_pdf(input_path: Path, ranges: list[tuple[int, int]] | None, output_path: Path) -> Path:
    reader = _read_pdf(input_path)
    page_count = len(reader.pages)

    if ranges is None:
        ranges = [(page, page) for page in range(1, page_count + 1)]

    pieces: list[tuple[str, PdfWriter]] = []
    for index, (start, end) in enumerate(ranges, start=1):
        writer = PdfWriter()
        for page_number in range(start, end + 1):
            writer.add_page(reader.pages[page_number - 1])
        name = f"{index:02d}_{start}-{end}.pdf" if start != end else f"{index:02d}_sayfa-{start}.pdf"
        pieces.append((name, writer))

    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for name, writer in pieces:
                piece_path = tmp_path / name
                with open(piece_path, "wb") as out:
                    writer.write(out)
                zip_file.write(piece_path, arcname=name)

    return output_path
