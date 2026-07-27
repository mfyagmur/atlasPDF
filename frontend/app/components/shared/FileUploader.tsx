import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { AnimatePresence, motion } from "motion/react";
import { ArrowDown, ArrowUp, X } from "lucide-react";
import { Button } from "../ui/button";
import { cn } from "~/lib/utils";

interface FileUploaderProps {
  files: File[];
  onFilesChange: (files: File[]) => void;
  accept?: Record<string, string[]>;
  multiple?: boolean;
}

export function FileUploader({
  files,
  onFilesChange,
  accept = { "application/pdf": [".pdf"] },
  multiple = true,
}: FileUploaderProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      onFilesChange([...files, ...acceptedFiles]);
    },
    [files, onFilesChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    multiple,
  });

  const removeFile = (index: number) => {
    onFilesChange(files.filter((_, i) => i !== index));
  };

  const moveFile = (index: number, direction: -1 | 1) => {
    const target = index + direction;
    if (target < 0 || target >= files.length) return;
    const next = [...files];
    [next[index], next[target]] = [next[target], next[index]];
    onFilesChange(next);
  };

  return (
    <div className="flex w-full flex-col gap-4">
      <div
        {...getRootProps()}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-border p-8 text-center transition-transform duration-150",
          isDragActive && "scale-[1.02] border-primary bg-muted"
        )}
      >
        <input {...getInputProps()} />
        <p className="text-sm text-muted-foreground">
          {isDragActive
            ? "Dosyaları buraya bırakın..."
            : "PDF dosyalarını sürükleyip bırakın veya seçmek için tıklayın"}
        </p>
      </div>

      {files.length > 0 && (
        <ul className="flex flex-col gap-2">
          <AnimatePresence mode="popLayout" initial={false}>
            {files.map((file, index) => (
              <motion.li
                key={`${file.name}-${index}`}
                layout
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 8, scale: 0.95 }}
                className="flex items-center justify-between gap-2 rounded-lg bg-muted px-3 py-2 text-sm"
              >
                <span className="truncate">{file.name}</span>
                <div className="flex shrink-0 items-center gap-1">
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon-sm"
                    disabled={index === 0}
                    onClick={() => moveFile(index, -1)}
                    aria-label="Yukarı taşı"
                  >
                    <ArrowUp />
                  </Button>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon-sm"
                    disabled={index === files.length - 1}
                    onClick={() => moveFile(index, 1)}
                    aria-label="Aşağı taşı"
                  >
                    <ArrowDown />
                  </Button>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon-sm"
                    onClick={() => removeFile(index)}
                    aria-label="Kaldır"
                  >
                    <X />
                  </Button>
                </div>
              </motion.li>
            ))}
          </AnimatePresence>
        </ul>
      )}
    </div>
  );
}
