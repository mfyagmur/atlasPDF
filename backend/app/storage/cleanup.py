import time
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

CLEANUP_INTERVAL_MINUTES = 10


def cleanup_expired_files(dirs: list[Path], ttl_minutes: int) -> None:
    cutoff = time.time() - (ttl_minutes * 60)
    for directory in dirs:
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.name == ".gitkeep" or not path.is_file():
                continue
            if path.stat().st_mtime < cutoff:
                path.unlink(missing_ok=True)


def start_cleanup_scheduler(upload_dir: Path, output_dir: Path, ttl_minutes: int) -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        cleanup_expired_files,
        "interval",
        minutes=CLEANUP_INTERVAL_MINUTES,
        args=[[upload_dir, output_dir], ttl_minutes],
    )
    scheduler.start()
    return scheduler
