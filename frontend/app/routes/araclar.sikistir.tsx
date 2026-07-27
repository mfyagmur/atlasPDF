import { useState } from "react";
import { AnimatePresence } from "motion/react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Label } from "../components/ui/label";
import { RadioGroup, RadioGroupItem } from "../components/ui/radio-group";
import { DownloadCard } from "../components/shared/DownloadCard";
import { ErrorBanner } from "../components/shared/ErrorBanner";
import { FileUploader } from "../components/shared/FileUploader";
import { ProgressIndicator } from "../components/shared/ProgressIndicator";
import type { Route } from "./+types/araclar.sikistir";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "PDF Sıkıştır — AtlasPDF" },
    { name: "description", content: "PDF dosyanızın boyutunu küçültün." },
  ];
}

type Status = "idle" | "uploading" | "success" | "error";
type CompressionLevel = "low" | "recommended" | "extreme";

const LEVELS: { value: CompressionLevel; title: string; description: string }[] = [
  { value: "low", title: "Düşük", description: "Az sıkıştırma, en yüksek kalite" },
  { value: "recommended", title: "Önerilen", description: "Kalite ve boyut arasında denge" },
  { value: "extreme", title: "Yüksek", description: "Agresif sıkıştırma, düşük kalite" },
];

function formatMB(bytes: number): string {
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export default function CompressPdfPage() {
  const [file, setFile] = useState<File | null>(null);
  const [level, setLevel] = useState<CompressionLevel>("recommended");
  const [status, setStatus] = useState<Status>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [originalSize, setOriginalSize] = useState<number | null>(null);
  const [compressedSize, setCompressedSize] = useState<number | null>(null);
  const [savingsPercent, setSavingsPercent] = useState<number | null>(null);

  const canCompress = file !== null && status !== "uploading";

  const handleFilesChange = (next: File[]) => {
    setFile(next[0] ?? null);
    setStatus("idle");
    setErrorMessage(null);
    setDownloadUrl(null);
    setOriginalSize(null);
    setCompressedSize(null);
    setSavingsPercent(null);
  };

  const handleCompress = async () => {
    if (!file) return;

    setStatus("uploading");
    setErrorMessage(null);
    setDownloadUrl(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("level", level);

    try {
      const response = await fetch(`${API_URL}/api/compress`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.detail ?? "Sıkıştırma sırasında bir hata oluştu.");
        setStatus("error");
        return;
      }

      setDownloadUrl(`${API_URL}${data.download_url}`);
      setOriginalSize(data.original_size);
      setCompressedSize(data.compressed_size);
      setSavingsPercent(data.savings_percent);
      setStatus("success");
    } catch {
      setErrorMessage("Sunucuya bağlanılamadı. Lütfen tekrar deneyin.");
      setStatus("error");
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 p-8">
      <div>
        <h1 className="text-3xl font-bold">PDF Sıkıştır</h1>
        <p className="text-muted-foreground">
          PDF dosyanızın boyutunu, kalite seviyesi seçerek küçültün.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Dosya</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-6">
          <FileUploader files={file ? [file] : []} onFilesChange={handleFilesChange} multiple={false} />

          {file && (
            <RadioGroup value={level} onValueChange={(value) => setLevel(value as CompressionLevel)}>
              <div className="flex flex-col gap-3">
                {LEVELS.map((option) => (
                  <label
                    key={option.value}
                    htmlFor={`level-${option.value}`}
                    className="flex cursor-pointer items-start gap-3 rounded-lg border p-4 hover:bg-accent"
                  >
                    <RadioGroupItem value={option.value} id={`level-${option.value}`} className="mt-1" />
                    <div className="flex flex-col gap-0.5">
                      <Label htmlFor={`level-${option.value}`} className="font-semibold">
                        {option.title}
                      </Label>
                      <span className="text-sm text-muted-foreground">{option.description}</span>
                    </div>
                  </label>
                ))}
              </div>
            </RadioGroup>
          )}

          {status === "uploading" && <ProgressIndicator label="Sıkıştırılıyor..." />}

          <AnimatePresence>
            {status === "error" && errorMessage && (
              <ErrorBanner key="error" message={errorMessage} />
            )}

            {status === "success" &&
              downloadUrl &&
              originalSize !== null &&
              compressedSize !== null &&
              savingsPercent !== null && (
                <DownloadCard
                  key="download"
                  downloadUrl={downloadUrl}
                  label="Sıkıştırılmış PDF'i İndir"
                  stats={
                    <p className="text-sm">
                      {formatMB(originalSize)} → {formatMB(compressedSize)}{" "}
                      <span className="font-semibold">(%{savingsPercent} küçültme)</span>
                    </p>
                  }
                />
              )}
          </AnimatePresence>

          <Button type="button" onClick={handleCompress} disabled={!canCompress}>
            Sıkıştır
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}
