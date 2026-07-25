import { Progress, ProgressLabel, ProgressValue } from "../ui/progress";

interface ProgressIndicatorProps {
  label: string;
  value?: number | null;
}

export function ProgressIndicator({ label, value = null }: ProgressIndicatorProps) {
  return (
    <Progress value={value} className="w-full">
      <div className="flex w-full justify-between">
        <ProgressLabel>{label}</ProgressLabel>
        {value !== null && <ProgressValue />}
      </div>
    </Progress>
  );
}
