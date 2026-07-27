import { useState } from "react";
import { AnimatePresence } from "motion/react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { RadioGroup, RadioGroupItem } from "../components/ui/radio-group";
import { DownloadCard } from "../components/shared/DownloadCard";
import { ErrorBanner } from "../components/shared/ErrorBanner";
import { FileUploader } from "../components/shared/FileUploader";
import { ProgressIndicator } from "../components/shared/ProgressIndicator";
import type { Route } from "./+types/araclar.bol";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "PDF Böl — AtlasPDF" },
    { name: "description", content: "PDF dosyasını sayfa aralıklarına göre bölün veya her sayfayı ayrı dosya yapın." },
  ];
}

type Status = "idle" | "uploading" | "success" | "error";
type SplitMode = "all" | "ranges";

export default function SplitPdfPage() {
  const [file, setFile] = useState<File | null>(null);
  const [pageCount, setPageCount] = useState<number | null>(null);
  const [mode, setMode] = useState<SplitMode>("all");
  const [ranges, setRanges] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

  const canSplit = file !== null && status !== "uploading" && (mode === "all" || ranges.trim().length > 0);

  const handleFilesChange = async (next: File[]) => {
    const nextFile = next[0] ?? null;
    setFile(nextFile);
    setPageCount(null);
    setStatus("idle");
    setErrorMessage(null);
    setDownloadUrl(null);

    if (!nextFile) return;

    const formData = new FormData();
    formData.append("file", nextFile);

    try {
      const response = await fetch(`${API_URL}/api/pdf-info`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.detail ?? "Dosya bilgisi alınamadı.");
        setStatus("error");
        return;
      }

      setPageCount(data.page_count);
    } catch {
      setErrorMessage("Sunucuya bağlanılamadı. Lütfen tekrar deneyin.");
      setStatus("error");
    }
  };

  const handleSplit = async () => {
    if (!file) return;

    setStatus("uploading");
    setErrorMessage(null);
    setDownloadUrl(null);

    const formData = new FormData();
    formData.append("file", file);
    if (mode === "ranges") {
      formData.append("ranges", ranges);
    }

    try {
      const response = await fetch(`${API_URL}/api/split`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.detail ?? "Bölme sırasında bir hata oluştu.");
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

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 p-8">
      <div>
        <h1 className="text-3xl font-bold">PDF Böl</h1>
        <p className="text-muted-foreground">
          Bir PDF dosyasını sayfa aralıklarına göre bölün veya her sayfayı ayrı dosya olarak çıkarın.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Dosya</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-6">
          <FileUploader
            files={file ? [file] : []}
            onFilesChange={(next) => void handleFilesChange(next)}
            multiple={false}
          />

          {pageCount !== null && (
            <p className="text-sm text-muted-foreground">Toplam sayfa sayısı: {pageCount}</p>
          )}

          {file && (
            <RadioGroup value={mode} onValueChange={(value) => setMode(value as SplitMode)}>
              <div className="flex items-center gap-2">
                <RadioGroupItem value="all" id="mode-all" />
                <Label htmlFor="mode-all">Her sayfayı ayır</Label>
              </div>
              <div className="flex items-center gap-2">
                <RadioGroupItem value="ranges" id="mode-ranges" />
                <Label htmlFor="mode-ranges">Aralık belirle</Label>
              </div>
            </RadioGroup>
          )}

          {file && mode === "ranges" && (
            <div className="flex flex-col gap-2">
              <Label htmlFor="ranges-input">Sayfa aralıkları</Label>
              <Input
                id="ranges-input"
                placeholder="1-3, 4-10"
                value={ranges}
                onChange={(event) => setRanges(event.target.value)}
              />
            </div>
          )}

          {status === "uploading" && <ProgressIndicator label="Bölünüyor..." />}

          <AnimatePresence>
            {status === "error" && errorMessage && (
              <ErrorBanner key="error" message={errorMessage} />
            )}

            {status === "success" && downloadUrl && (
              <DownloadCard key="download" downloadUrl={downloadUrl} label="Bölünmüş Dosyaları İndir (ZIP)" />
            )}
          </AnimatePresence>

          <Button type="button" onClick={handleSplit} disabled={!canSplit}>
            Böl
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}
