import uuid
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request, UploadFile

from app.core.config import settings
from app.core.limiter import RATE_LIMIT, limiter
from app.core.logging import log_tool_call
from app.storage.exceptions import FileTooLargeError, InvalidFileTypeError
from app.storage.utils import save_upload
from app.tools.split.exceptions import InvalidPageRangeError, InvalidPDFError
from app.tools.split.service import get_page_count, parse_ranges, split_pdf

router = APIRouter()

MAX_TOTAL_BYTES = settings.max_total_upload_mb * 1024 * 1024


@router.post("/api/pdf-info")
@limiter.limit(RATE_LIMIT)
async def pdf_info_endpoint(request: Request, file: UploadFile) -> dict[str, int]:
    path: Path | None = None
    try:
        try:
            path, _ = await save_upload(file, settings.upload_dir, MAX_TOTAL_BYTES)
        except InvalidFileTypeError as exc:
            raise HTTPException(status_code=415, detail=str(exc)) from exc
        except FileTooLargeError as exc:
            raise HTTPException(status_code=413, detail=str(exc)) from exc

        try:
            page_count = get_page_count(path)
        except InvalidPDFError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        return {"page_count": page_count}
    finally:
        if path is not None:
            path.unlink(missing_ok=True)


@router.post("/api/split")
@limiter.limit(RATE_LIMIT)
@log_tool_call("split")
async def split_endpoint(request: Request, file: UploadFile, ranges: str | None = Form(None)) -> dict[str, str]:
    saved_path: Path | None = None

    try:
        try:
            saved_path, _ = await save_upload(file, settings.upload_dir, MAX_TOTAL_BYTES)
        except InvalidFileTypeError as exc:
            raise HTTPException(status_code=415, detail=str(exc)) from exc
        except FileTooLargeError as exc:
            raise HTTPException(status_code=413, detail=str(exc)) from exc

        try:
            page_count = get_page_count(saved_path)
        except InvalidPDFError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        parsed_ranges: list[tuple[int, int]] | None = None
        if ranges:
            try:
                parsed_ranges = parse_ranges(ranges, page_count)
            except InvalidPageRangeError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

        output_id = uuid.uuid4()
        output_path = settings.output_dir / f"{output_id}.zip"

        try:
            split_pdf(saved_path, parsed_ranges, output_path)
        except InvalidPDFError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        return {
            "file_id": str(output_id),
            "download_url": f"/api/download/{output_id}",
        }
    finally:
        if saved_path is not None:
            saved_path.unlink(missing_ok=True)
