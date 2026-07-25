from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from app.tools.merge.exceptions import InvalidPDFError


def merge_pdfs(input_paths: list[Path], output_path: Path) -> Path:
    writer = PdfWriter()

    for path in input_paths:
        try:
            reader = PdfReader(path)
        except PdfReadError as exc:
            raise InvalidPDFError(f"Bozuk PDF dosyası: {path.name}") from exc

        if reader.is_encrypted:
            raise InvalidPDFError(f"Şifreli PDF dosyası desteklenmiyor: {path.name}")

        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as out:
        writer.write(out)

    return output_path
