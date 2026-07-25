import { useEffect, useState } from "react";
import { Button } from "../ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

type HealthStatus = "loading" | "ok" | "error";

export function HealthCheck() {
  const [status, setStatus] = useState<HealthStatus>("loading");

  const checkHealth = () => {
    setStatus("loading");
    fetch(`${API_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status === "ok" ? "ok" : "error"))
      .catch(() => setStatus("error"));
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Backend Bağlantısı</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <p>
          Durum:{" "}
          {status === "loading" && "kontrol ediliyor..."}
          {status === "ok" && "✅ bağlı"}
          {status === "error" && "❌ bağlanamadı"}
        </p>
        <Button onClick={checkHealth}>Tekrar Kontrol Et</Button>
      </CardContent>
    </Card>
  );
}
