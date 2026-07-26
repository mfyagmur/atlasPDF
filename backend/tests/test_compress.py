import io

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfReader, PdfWriter

from app.main import app
from app.tools.compress import service as compress_service

client = TestClient(app)


def make_pdf_bytes(num_pages: int = 3) -> bytes:
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


@pytest.mark.parametrize("level", ["low", "recommended", "extreme"])
def test_compress_happy_path_each_level(level):
    pdf = make_pdf_bytes(3)

    response = client.post(
        "/api/compress",
        files={"file": ("a.pdf", pdf, "application/pdf")},
        data={"level": level},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["download_url"] == f"/api/download/{data['file_id']}"
    assert data["original_size"] > 0
    assert data["compressed_size"] > 0
    assert data["savings_percent"] >= 0

    download = client.get(data["download_url"])
    assert download.status_code == 200
    assert download.headers["content-type"] == "application/pdf"

    compressed = PdfReader(io.BytesIO(download.content))
    assert len(compressed.pages) == 3


def test_compress_rejects_non_pdf_file():
    fake = b"hello world, this is not a pdf"

    response = client.post(
        "/api/compress",
        files={"file": ("fake.pdf", fake, "application/pdf")},
        data={"level": "recommended"},
    )

    assert response.status_code == 415


def test_compress_falls_back_to_pikepdf_without_ghostscript(tmp_path, monkeypatch):
    monkeypatch.setattr(compress_service, "find_ghostscript", lambda: None)

    input_path = tmp_path / "input.pdf"
    input_path.write_bytes(make_pdf_bytes(2))
    output_path = tmp_path / "output.pdf"

    result = compress_service.compress_pdf(input_path, output_path, "recommended")

    assert result.output_path == output_path
    assert output_path.exists()
    compressed = PdfReader(output_path)
    assert len(compressed.pages) == 2
