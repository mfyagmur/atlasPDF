import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { DownloadCard } from "../components/shared/DownloadCard";
import { ErrorBanner } from "../components/shared/ErrorBanner";
import { FileUploader } from "../components/shared/FileUploader";
import { ProgressIndicator } from "../components/shared/ProgressIndicator";
import type { Route } from "./+types/araclar.pdf-excel";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "PDF'i Excel'e Çevir — AtlasPDF" },
    { name: "description", content: "PDF içindeki tabloları düzenlenebilir Excel (.xlsx) dosyasına çıkarın." },
  ];
}

type Status = "idle" | "uploading" | "success" | "error";

export default function PdfToExcelPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);
  const [tablesFound, setTablesFound] = useState<number | null>(null);

  const canConvert = file !== null && status !== "uploading";

  const handleFilesChange = (next: File[]) => {
    setFile(next[0] ?? null);
    setStatus("idle");
    setErrorMessage(null);
    setDownloadUrl(null);
    setWarning(null);
    setTablesFound(null);
  };

  const handleConvert = async () => {
    if (!file) return;

    setStatus("uploading");
    setErrorMessage(null);
    setDownloadUrl(null);
    setWarning(null);
    setTablesFound(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/api/pdf-to-excel`, {
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
      setTablesFound(data.tables_found);
      setStatus("success");
    } catch {
      setErrorMessage("Sunucuya bağlanılamadı. Lütfen tekrar deneyin.");
      setStatus("error");
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 p-8">
      <div>
        <h1 className="text-3xl font-bold">PDF'i Excel'e Çevir</h1>
        <p className="text-muted-foreground">
          PDF içindeki tabloları düzenlenebilir bir Excel (.xlsx) dosyasına çıkarın.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Dosya</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-6">
          <FileUploader files={file ? [file] : []} onFilesChange={handleFilesChange} multiple={false} />

          {status === "uploading" && <ProgressIndicator label="Dönüştürülüyor..." />}

          {status === "error" && errorMessage && <ErrorBanner message={errorMessage} />}

          {status === "success" && warning && <ErrorBanner variant="warning" message={warning} />}

          {status === "success" && downloadUrl && tablesFound !== null && (
            <DownloadCard
              downloadUrl={downloadUrl}
              label="Excel Dosyasını İndir"
              stats={
                <p className="text-sm">
                  {tablesFound > 0 ? `${tablesFound} tablo bulundu.` : "Tablo bulunamadı."}
                </p>
              }
            />
          )}

          <Button type="button" onClick={handleConvert} disabled={!canConvert}>
            Excel'e Çevir
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}
