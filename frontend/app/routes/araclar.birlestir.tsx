import { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { FileUploader } from "../components/shared/FileUploader";
import { ProgressIndicator } from "../components/shared/ProgressIndicator";
import type { Route } from "./+types/araclar.birlestir";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "PDF Birleştir — AtlasPDF" },
    { name: "description", content: "Birden fazla PDF dosyasını tek dosyada birleştirin." },
  ];
}

type Status = "idle" | "uploading" | "success" | "error";

export default function MergePdfPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [status, setStatus] = useState<Status>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

  const canMerge = files.length >= 2 && status !== "uploading";

  const handleMerge = async () => {
    setStatus("uploading");
    setErrorMessage(null);
    setDownloadUrl(null);

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const response = await fetch(`${API_URL}/api/merge`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.detail ?? "Birleştirme sırasında bir hata oluştu.");
        setStatus("error");
        return;
      }

      setDownloadUrl(`${API_URL}${data.download_url}`);
      setStatus("success");
    } catch {
      setErrorMessage("Sunucuya bağlanılamadı. Lütfen tekrar deneyin.");
      setStatus("error");
    }
  };

  const handleFilesChange = (next: File[]) => {
    setFiles(next);
    setStatus("idle");
    setErrorMessage(null);
    setDownloadUrl(null);
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 p-8">
      <div>
        <h1 className="text-3xl font-bold">PDF Birleştir</h1>
        <p className="text-muted-foreground">
          Birden fazla PDF dosyasını istediğiniz sırada tek bir dosyada birleştirin.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Dosyalar</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-6">
          <FileUploader files={files} onFilesChange={handleFilesChange} />

          {status === "uploading" && <ProgressIndicator label="Birleştiriliyor..." />}

          {status === "error" && errorMessage && (
            <p className="text-sm text-destructive">{errorMessage}</p>
          )}

          {status === "success" && downloadUrl && (
            <a href={downloadUrl} download>
              <Button type="button" variant="secondary" className="w-full">
                Birleştirilmiş PDF'i İndir
              </Button>
            </a>
          )}

          <Button type="button" onClick={handleMerge} disabled={!canMerge}>
            Birleştir
          </Button>

          {files.length === 1 && (
            <p className="text-sm text-muted-foreground">
              Birleştirmek için en az 2 PDF dosyası yükleyin.
            </p>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
