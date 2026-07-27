import logging
import time
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger("atlaspdf.cleanup")


def cleanup_expired_files(dirs: list[Path], ttl_minutes: int) -> int:
    cutoff = time.time() - (ttl_minutes * 60)
    deleted_count = 0
    for directory in dirs:
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.name == ".gitkeep" or not path.is_file():
                continue
            if path.stat().st_mtime < cutoff:
                path.unlink(missing_ok=True)
                deleted_count += 1

    logger.info("cleanup_run_completed", extra={"deleted_count": deleted_count, "ttl_minutes": ttl_minutes})
    return deleted_count


def start_cleanup_scheduler(
    upload_dir: Path, output_dir: Path, ttl_minutes: int, interval_minutes: int
) -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        cleanup_expired_files,
        "interval",
        minutes=interval_minutes,
        args=[[upload_dir, output_dir], ttl_minutes],
    )
    scheduler.start()
    return scheduler
