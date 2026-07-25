import io

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app

client = TestClient(app)


def make_pdf_bytes(num_pages: int = 1) -> bytes:
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_merge_happy_path():
    pdf_a = make_pdf_bytes(1)
    pdf_b = make_pdf_bytes(2)

    response = client.post(
        "/api/merge",
        files=[
            ("files", ("a.pdf", pdf_a, "application/pdf")),
            ("files", ("b.pdf", pdf_b, "application/pdf")),
        ],
    )

    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["download_url"] == f"/api/download/{data['file_id']}"

    download = client.get(data["download_url"])
    assert download.status_code == 200
    assert download.headers["content-type"] == "application/pdf"

    from pypdf import PdfReader

    merged = PdfReader(io.BytesIO(download.content))
    assert len(merged.pages) == 3


def test_merge_requires_at_least_two_files():
    pdf_a = make_pdf_bytes(1)

    response = client.post(
        "/api/merge",
        files=[("files", ("a.pdf", pdf_a, "application/pdf"))],
    )

    assert response.status_code == 400


def test_merge_rejects_non_pdf_file():
    pdf_a = make_pdf_bytes(1)
    fake = b"hello world, this is not a pdf"

    response = client.post(
        "/api/merge",
        files=[
            ("files", ("a.pdf", pdf_a, "application/pdf")),
            ("files", ("fake.pdf", fake, "application/pdf")),
        ],
    )

    assert response.status_code == 415
