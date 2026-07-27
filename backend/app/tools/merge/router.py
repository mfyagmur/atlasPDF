import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, UploadFile

from app.core.config import settings
from app.core.limiter import RATE_LIMIT, limiter
from app.core.logging import log_tool_call
from app.storage.exceptions import FileTooLargeError, InvalidFileTypeError
from app.storage.utils import save_upload
from app.tools.merge.exceptions import InvalidPDFError
from app.tools.merge.service import merge_pdfs

router = APIRouter()

MAX_TOTAL_BYTES = settings.max_total_upload_mb * 1024 * 1024


@router.post("/api/merge")
@limiter.limit(RATE_LIMIT)
@log_tool_call("merge")
async def merge_endpoint(request: Request, files: list[UploadFile]) -> dict[str, str]:
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Birleştirmek için en az 2 PDF dosyası yükleyin.")

    saved_paths: list[Path] = []
    remaining_bytes = MAX_TOTAL_BYTES

    try:
        input_paths = []
        for file in files:
            try:
                path, bytes_written = await save_upload(file, settings.upload_dir, remaining_bytes)
            except InvalidFileTypeError as exc:
                raise HTTPException(status_code=415, detail=str(exc)) from exc
            except FileTooLargeError as exc:
                raise HTTPException(status_code=413, detail=str(exc)) from exc

            input_paths.append(path)
            saved_paths.append(path)
            remaining_bytes -= bytes_written

        output_id = uuid.uuid4()
        output_path = settings.output_dir / f"{output_id}.pdf"

        try:
            merge_pdfs(input_paths, output_path)
        except InvalidPDFError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        return {
            "file_id": str(output_id),
            "download_url": f"/api/download/{output_id}",
        }
    finally:
        for path in saved_paths:
            path.unlink(missing_ok=True)
