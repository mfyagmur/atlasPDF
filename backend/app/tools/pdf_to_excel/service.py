from dataclasses import dataclass
from pathlib import Path

import pdfplumber
from openpyxl import Workbook
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.tools.pdf_to_excel.exceptions import InvalidPDFError

NO_TABLE_WARNING = "Tablo tespit edilemedi, metin çıkarıldı."
MAX_SHEET_NAME_LENGTH = 31
MAX_CELL_LENGTH = 200
MAX_CELL_NEWLINES = 5
MIN_TEXT_LINE_LENGTH = 3
WATERMARK_BRIGHTNESS_THRESHOLD = 0.7
WATERMARK_COLOR_SPREAD_THRESHOLD = 0.15

TABLE_STRATEGIES = [
    {"vertical_strategy": "lines", "horizontal_strategy": "lines"},
    {"vertical_strategy": "text", "horizontal_strategy": "text"},
]


def _is_watermark_color(color: object) -> bool:
    values = color if isinstance(color, (list, tuple)) else (color,)
    if not values or not all(isinstance(v, (int, float)) for v in values):
        return False

    brightness = sum(values) / len(values)
    spread = max(values) - min(values)
    return spread < WATERMARK_COLOR_SPREAD_THRESHOLD and brightness > WATERMARK_BRIGHTNESS_THRESHOLD


def _is_real_char(obj: dict) -> bool:
    if obj["object_type"] != "char":
        return True
    if not obj.get("upright", True):
        return False
    return not _is_watermark_color(obj.get("non_stroking_color"))


def _is_valid_table(rows: list[list[str | None]]) -> bool:
    if len(rows) > 1:
        return True
    for row in rows:
        for cell in row:
            if cell and (len(cell) > MAX_CELL_LENGTH or cell.count("\n") >= MAX_CELL_NEWLINES):
                return False
    return True


def _find_valid_tables(page) -> tuple[list, list[list[list[str | None]]]]:
    for settings in TABLE_STRATEGIES:
        found = page.find_tables(table_settings=settings)
        if not found:
            continue
        extracted = [table.extract() for table in found]
        if all(_is_valid_table(rows) for rows in extracted):
            return found, extracted
    return [], []


def _extract_text_lines(page) -> list[str]:
    text = page.extract_text() or ""
    return [line for line in text.splitlines() if len(line.strip()) >= MIN_TEXT_LINE_LENGTH]


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


def _sheet_name(page_number: int) -> str:
    name = f"Sayfa{page_number}"
    return name[:MAX_SHEET_NAME_LENGTH]


def pdf_to_excel(input_path: Path, output_path: Path) -> ExcelResult:
    _read_pdf(input_path)

    workbook = Workbook()
    workbook.remove(workbook.active)
    tables_found = 0

    try:
        with pdfplumber.open(input_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                sheet = workbook.create_sheet(title=_sheet_name(page_number))
                clean_page = page.filter(_is_real_char)
                found_tables, extracted_tables = _find_valid_tables(clean_page)

                if found_tables:
                    tables_found += len(found_tables)
                    bboxes = [t.bbox for t in found_tables]

                    def _outside_tables(obj: dict, bboxes: list = bboxes) -> bool:
                        return not any(
                            obj["x0"] >= x0 and obj["x1"] <= x1 and obj["top"] >= top and obj["bottom"] <= bottom
                            for x0, top, x1, bottom in bboxes
                        )

                    for table_index, rows in enumerate(extracted_tables):
                        if table_index > 0:
                            sheet.append([])
                        for row in rows:
                            sheet.append(row)

                    remaining_text = (clean_page.filter(_outside_tables).extract_text() or "").strip()
                    if remaining_text:
                        sheet.append([])
                        for line in remaining_text.splitlines():
                            if len(line.strip()) >= MIN_TEXT_LINE_LENGTH:
                                sheet.append([line])
                else:
                    for line in _extract_text_lines(clean_page):
                        sheet.append([line])

            warning = NO_TABLE_WARNING if tables_found == 0 else None

        workbook.save(output_path)
    except Exception as exc:
        raise InvalidPDFError(f"PDF Excel'e dönüştürülemedi: {input_path.name}") from exc

    return ExcelResult(output_path=output_path, tables_found=tables_found, warning=warning)
