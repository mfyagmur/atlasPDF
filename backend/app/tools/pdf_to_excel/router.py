import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.core.config import settings
from app.storage.exceptions import FileTooLargeError, InvalidFileTypeError
from app.storage.utils import save_upload
from app.tools.pdf_to_excel.exceptions import InvalidPDFError
from app.tools.pdf_to_excel.service import pdf_to_excel

router = APIRouter()

MAX_TOTAL_BYTES = settings.max_total_upload_mb * 1024 * 1024


@router.post("/api/pdf-to-excel")
async def pdf_to_excel_endpoint(file: UploadFile) -> dict[str, str | int | None]:
    saved_path: Path | None = None

    try:
        try:
            saved_path, _ = await save_upload(file, settings.upload_dir, MAX_TOTAL_BYTES)
        except InvalidFileTypeError as exc:
            raise HTTPException(status_code=415, detail=str(exc)) from exc
        except FileTooLargeError as exc:
            raise HTTPException(status_code=413, detail=str(exc)) from exc

        output_id = uuid.uuid4()
        output_path = settings.output_dir / f"{output_id}.xlsx"

        try:
            result = pdf_to_excel(saved_path, output_path)
        except InvalidPDFError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        return {
            "file_id": str(output_id),
            "download_url": f"/api/download/{output_id}",
            "tables_found": result.tables_found,
            "warning": result.warning,
        }
    finally:
        if saved_path is not None:
            saved_path.unlink(missing_ok=True)
