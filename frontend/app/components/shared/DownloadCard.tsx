import type { ReactNode } from "react";
import { Button } from "../ui/button";

type DownloadCardProps = {
  downloadUrl: string;
  label: string;
  stats?: ReactNode;
};

export function DownloadCard({ downloadUrl, label, stats }: DownloadCardProps) {
  const button = (
    <a href={downloadUrl} download>
      <Button type="button" variant="secondary" className="w-full">
        {label}
      </Button>
    </a>
  );

  if (!stats) {
    return button;
  }

  return (
    <div className="flex flex-col gap-3 rounded-lg border p-4">
      {stats}
      {button}
    </div>
  );
}
