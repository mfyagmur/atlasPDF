import io
import zipfile

import pikepdf
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app

client = TestClient(app)


def make_blank_pdf_bytes(num_pages: int = 1) -> bytes:
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def make_text_pdf_bytes(text: str = "Hello World, this is a real text-based PDF page.", num_pages: int = 1) -> bytes:
    pdf = pikepdf.Pdf.new()
    for _ in range(num_pages):
        page = pdf.add_blank_page(page_size=(400, 400))
        content = f"BT /F1 24 Tf 72 300 Td ({text}) Tj ET".encode()
        stream = pdf.make_stream(content)
        font = pikepdf.Dictionary(
            Type=pikepdf.Name.Font,
            Subtype=pikepdf.Name.Type1,
            BaseFont=pikepdf.Name.Helvetica,
        )
        page.obj.Resources = pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font))
        page.obj.Contents = stream

    buffer = io.BytesIO()
    pdf.save(buffer)
    return buffer.getvalue()


def make_encrypted_pdf_bytes() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.encrypt("secret")
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_pdf_to_word_happy_path():
    pdf = make_text_pdf_bytes()

    response = client.post(
        "/api/pdf-to-word",
        files={"file": ("a.pdf", pdf, "application/pdf")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["download_url"] == f"/api/download/{data['file_id']}"
    assert data["warning"] is None

    download = client.get(data["download_url"])
    assert download.status_code == 200
    assert download.headers["content-type"] == (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert zipfile.is_zipfile(io.BytesIO(download.content))


def test_pdf_to_word_scanned_pdf_returns_warning():
    pdf = make_blank_pdf_bytes(2)

    response = client.post(
        "/api/pdf-to-word",
        files={"file": ("scanned.pdf", pdf, "application/pdf")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["warning"] is not None

    download = client.get(data["download_url"])
    assert download.status_code == 200


def test_pdf_to_word_rejects_non_pdf_file():
    fake = b"hello world, this is not a pdf"

    response = client.post(
        "/api/pdf-to-word",
        files={"file": ("fake.pdf", fake, "application/pdf")},
    )

    assert response.status_code == 415


def test_pdf_to_word_rejects_encrypted_pdf():
    pdf = make_encrypted_pdf_bytes()

    response = client.post(
        "/api/pdf-to-word",
        files={"file": ("encrypted.pdf", pdf, "application/pdf")},
    )

    assert response.status_code == 422
    assert "Şifreli" in response.json()["detail"]
