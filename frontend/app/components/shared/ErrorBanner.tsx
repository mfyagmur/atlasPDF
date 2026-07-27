import { motion } from "motion/react";

type ErrorBannerProps = {
  message: string;
  variant?: "error" | "warning";
};

const fadeInScale = {
  initial: { opacity: 0, scale: 0.97 },
  animate: { opacity: 1, scale: 1 },
};

export function ErrorBanner({ message, variant = "error" }: ErrorBannerProps) {
  if (variant === "warning") {
    return (
      <motion.div
        {...fadeInScale}
        className="rounded-lg border border-amber-400 bg-amber-50 p-4 text-sm text-amber-900 dark:border-amber-700 dark:bg-amber-950 dark:text-amber-200"
      >
        {message}
      </motion.div>
    );
  }

  return (
    <motion.p {...fadeInScale} className="text-sm text-destructive">
      {message}
    </motion.p>
  );
}
