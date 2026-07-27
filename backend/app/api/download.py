from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.limiter import RATE_LIMIT, limiter

router = APIRouter()

MEDIA_TYPES = {
    ".zip": "application/zip",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


@router.get("/api/download/{file_id}")
@limiter.limit(RATE_LIMIT)
async def download_file(request: Request, file_id: str) -> FileResponse:
    matches = list(settings.output_dir.glob(f"{file_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Dosya bulunamadı veya süresi doldu.")

    path = matches[0]
    media_type = MEDIA_TYPES.get(path.suffix, "application/pdf")
    return FileResponse(path, media_type=media_type, filename=f"atlaspdf{path.suffix}")
