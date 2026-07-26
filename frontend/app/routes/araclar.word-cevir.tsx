import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { FileUploader } from "../components/shared/FileUploader";
import { ProgressIndicator } from "../components/shared/ProgressIndicator";
import type { Route } from "./+types/araclar.word-cevir";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const SLOW_PAGE_COUNT_THRESHOLD = 30;

export function meta({}: Route.MetaArgs) {
  return [
    { title: "PDF'i Word'e Çevir — AtlasPDF" },
    { name: "description", content: "PDF dosyanızı düzenlenebilir Word (.docx) belgesine çevirin." },
  ];
}

type Status = "idle" | "uploading" | "success" | "error";

export default function PdfToWordPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);
  const [pageCount, setPageCount] = useState<number | null>(null);

  const canConvert = file !== null && status !== "uploading";

  const handleFilesChange = async (next: File[]) => {
    const nextFile = next[0] ?? null;
    setFile(nextFile);
    setStatus("idle");
    setErrorMessage(null);
    setDownloadUrl(null);
    setWarning(null);
    setPageCount(null);

    if (!nextFile) return;

    const formData = new FormData();
    formData.append("file", nextFile);

    try {
      const response = await fetch(`${API_URL}/api/pdf-info`, {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        setPageCount(data.page_count);
      }
    } catch {
      // Sayfa sayısı alınamazsa sessizce geç, dönüştürme işlemini engellemez.
    }
  };

  const handleConvert = async () => {
    if (!file) return;

    setStatus("uploading");
    setErrorMessage(null);
    setDownloadUrl(null);
    setWarning(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/api/pdf-to-word`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.detail ?? "Dönüştürme sırasında bir hata oluştu.");
        setStatus("error");
        return;
      }

      setDownloadUrl(`${API_URL}${data.download_url}`);
      setWarning(data.warning ?? null);
      setStatus("success");
    } catch {
      setErrorMessage("Sunucuya bağlanılamadı. Lütfen tekrar deneyin.");
      setStatus("error");
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 p-8">
      <div>
        <h1 className="text-3xl font-bold">PDF'i Word'e Çevir</h1>
        <p className="text-muted-foreground">
          PDF dosyanızı düzenlenebilir bir Word (.docx) belgesine dönüştürün.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Dosya</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-6">
          <FileUploader files={file ? [file] : []} onFilesChange={handleFilesChange} multiple={false} />

          {file && pageCount !== null && pageCount > SLOW_PAGE_COUNT_THRESHOLD && (
            <p className="text-sm text-muted-foreground">
              Bu dosya {pageCount} sayfa, işlem biraz sürebilir.
            </p>
          )}

          {status === "uploading" && <ProgressIndicator label="Dönüştürülüyor..." />}

          {status === "error" && errorMessage && (
            <p className="text-sm text-destructive">{errorMessage}</p>
          )}

          {status === "success" && warning && (
            <div className="rounded-lg border border-amber-400 bg-amber-50 p-4 text-sm text-amber-900 dark:border-amber-700 dark:bg-amber-950 dark:text-amber-200">
              {warning}
            </div>
          )}

          {status === "success" && downloadUrl && (
            <div className="flex flex-col gap-3 rounded-lg border p-4">
              <a href={downloadUrl} download>
                <Button type="button" variant="secondary" className="w-full">
                  Word Dosyasını İndir
                </Button>
              </a>
            </div>
          )}

          <Button type="button" onClick={handleConvert} disabled={!canConvert}>
            Word'e Çevir
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}
