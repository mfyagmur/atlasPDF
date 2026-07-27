from dataclasses import dataclass
from pathlib import Path

import pdfplumber
from openpyxl import Workbook
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.tools.pdf_to_excel.exceptions import InvalidPDFError

NO_TABLE_WARNING = "Tablo tespit edilemedi, metin çıkarıldı."
MAX_SHEET_NAME_LENGTH = 31


def _read_pdf(input_path: Path) -> PdfReader:
    try:
        reader = PdfReader(input_path)
    except PdfReadError as exc:
        raise InvalidPDFError(f"Bozuk PDF dosyası: {input_path.name}") from exc

    if reader.is_encrypted:
        raise InvalidPDFError(f"Şifreli PDF dosyası desteklenmiyor: {input_path.name}")

    return reader


@dataclass
class ExcelResult:
    output_path: Path
    tables_found: int
    warning: str | None


def _sheet_name(page_number: int, table_number: int) -> str:
    name = f"Sayfa{page_number}_Tablo{table_number}"
    return name[:MAX_SHEET_NAME_LENGTH]


def pdf_to_excel(input_path: Path, output_path: Path) -> ExcelResult:
    _read_pdf(input_path)

    workbook = Workbook()
    workbook.remove(workbook.active)
    tables_found = 0

    try:
        with pdfplumber.open(input_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table_number, table in enumerate(tables, start=1):
                    tables_found += 1
                    sheet = workbook.create_sheet(title=_sheet_name(page_number, table_number))
                    for row in table:
                        sheet.append(row)

            warning = None
            if tables_found == 0:
                sheet = workbook.create_sheet(title="Metin")
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    for line in text.splitlines():
                        sheet.append([line])
                warning = NO_TABLE_WARNING

        workbook.save(output_path)
    except Exception as exc:
        raise InvalidPDFError(f"PDF Excel'e dönüştürülemedi: {input_path.name}") from exc

    return ExcelResult(output_path=output_path, tables_found=tables_found, warning=warning)
