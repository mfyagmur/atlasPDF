type ErrorBannerProps = {
  message: string;
  variant?: "error" | "warning";
};

export function ErrorBanner({ message, variant = "error" }: ErrorBannerProps) {
  if (variant === "warning") {
    return (
      <div className="rounded-lg border border-amber-400 bg-amber-50 p-4 text-sm text-amber-900 dark:border-amber-700 dark:bg-amber-950 dark:text-amber-200">
        {message}
      </div>
    );
  }

  return <p className="text-sm text-destructive">{message}</p>;
}
