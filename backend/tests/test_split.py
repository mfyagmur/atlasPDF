import io
import zipfile

from fastapi.testclient import TestClient
from pypdf import PdfReader, PdfWriter

from app.main import app

client = TestClient(app)


def make_pdf_bytes(num_pages: int = 1) -> bytes:
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_split_happy_path_ranges():
    pdf = make_pdf_bytes(4)

    response = client.post(
        "/api/split",
        files={"file": ("a.pdf", pdf, "application/pdf")},
        data={"ranges": "1-2,3-4"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["download_url"] == f"/api/download/{data['file_id']}"

    download = client.get(data["download_url"])
    assert download.status_code == 200
    assert download.headers["content-type"] == "application/zip"

    zf = zipfile.ZipFile(io.BytesIO(download.content))
    names = zf.namelist()
    assert len(names) == 2

    for name in names:
        piece = PdfReader(io.BytesIO(zf.read(name)))
        assert len(piece.pages) == 2


def test_split_happy_path_all_pages():
    pdf = make_pdf_bytes(3)

    response = client.post(
        "/api/split",
        files={"file": ("a.pdf", pdf, "application/pdf")},
    )

    assert response.status_code == 200
    data = response.json()

    download = client.get(data["download_url"])
    assert download.status_code == 200

    zf = zipfile.ZipFile(io.BytesIO(download.content))
    names = zf.namelist()
    assert len(names) == 3

    for name in names:
        piece = PdfReader(io.BytesIO(zf.read(name)))
        assert len(piece.pages) == 1


def test_split_range_exceeds_page_count():
    pdf = make_pdf_bytes(3)

    response = client.post(
        "/api/split",
        files={"file": ("a.pdf", pdf, "application/pdf")},
        data={"ranges": "1-5"},
    )

    assert response.status_code == 400


def test_split_rejects_malformed_range():
    pdf = make_pdf_bytes(3)

    response = client.post(
        "/api/split",
        files={"file": ("a.pdf", pdf, "application/pdf")},
        data={"ranges": "abc"},
    )

    assert response.status_code == 400


def test_pdf_info_returns_page_count():
    pdf = make_pdf_bytes(5)

    response = client.post(
        "/api/pdf-info",
        files={"file": ("a.pdf", pdf, "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json() == {"page_count": 5}
