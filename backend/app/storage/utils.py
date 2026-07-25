import uuid
from pathlib import Path

from fastapi import UploadFile

from app.storage.exceptions import FileTooLargeError, InvalidFileTypeError

PDF_MAGIC = b"%PDF-"
CHUNK_SIZE = 1024 * 1024  # 1MB


def looks_like_pdf(header: bytes) -> bool:
    return header.startswith(PDF_MAGIC)


async def save_upload(file: UploadFile, dest_dir: Path, max_bytes: int) -> tuple[Path, int]:
    """Yüklenen dosyayı UUID isimle dest_dir altına kaydeder.

    İlk chunk'ta PDF header kontrolü yapar ve toplam boyutu max_bytes ile sınırlar.
    Doğrulama başarısız olursa kısmi dosyayı siler ve ilgili exception'ı fırlatır.
    """
    dest_path = dest_dir / f"{uuid.uuid4()}.pdf"
    bytes_written = 0
    first_chunk = True

    with open(dest_path, "wb") as out:
        while True:
            chunk = await file.read(CHUNK_SIZE)
            if not chunk:
                break
            if first_chunk:
                if not looks_like_pdf(chunk[: len(PDF_MAGIC)]):
                    out.close()
                    dest_path.unlink(missing_ok=True)
                    raise InvalidFileTypeError(f"'{file.filename}' geçerli bir PDF dosyası değil.")
                first_chunk = False

            bytes_written += len(chunk)
            if bytes_written > max_bytes:
                out.close()
                dest_path.unlink(missing_ok=True)
                raise FileTooLargeError("Toplam dosya boyutu izin verilen limiti aşıyor.")

            out.write(chunk)

    if first_chunk:
        # Dosya tamamen boştu, hiç chunk okunmadı.
        dest_path.unlink(missing_ok=True)
        raise InvalidFileTypeError(f"'{file.filename}' geçerli bir PDF dosyası değil.")

    return dest_path, bytes_written
