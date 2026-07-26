from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.download import router as download_router
from app.core.config import settings
from app.storage.cleanup import start_cleanup_scheduler
from app.tools.compress.router import router as compress_router
from app.tools.merge.router import router as merge_router
from app.tools.pdf_to_word.router import router as pdf_to_word_router
from app.tools.split.router import router as split_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    scheduler = start_cleanup_scheduler(settings.upload_dir, settings.output_dir, settings.file_ttl_minutes)
    yield
    scheduler.shutdown()


app = FastAPI(title="AtlasPDF API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(merge_router)
app.include_router(split_router)
app.include_router(compress_router)
app.include_router(pdf_to_word_router)
app.include_router(download_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
