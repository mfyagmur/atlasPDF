from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings

router = APIRouter()

MEDIA_TYPES = {
    ".zip": "application/zip",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.get("/api/download/{file_id}")
async def download_file(file_id: str) -> FileResponse:
    matches = list(settings.output_dir.glob(f"{file_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Dosya bulunamadı veya süresi doldu.")

    path = matches[0]
    media_type = MEDIA_TYPES.get(path.suffix, "application/pdf")
    return FileResponse(path, media_type=media_type, filename=f"atlaspdf{path.suffix}")
