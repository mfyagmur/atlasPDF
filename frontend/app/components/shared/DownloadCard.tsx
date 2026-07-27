import type { ReactNode } from "react";
import { motion } from "motion/react";
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
    return (
      <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }}>
        {button}
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col gap-3 rounded-lg border p-4"
    >
      {stats}
      {button}
    </motion.div>
  );
}
