import json
import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from app.core.config import settings

_RESERVED = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _RESERVED:
                payload[key] = value
        return json.dumps(payload, default=str)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    if settings.log_json:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(settings.log_level)


logger = logging.getLogger("atlaspdf.tools")

F = TypeVar("F", bound=Callable[..., Any])


def log_tool_call(tool_name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
            except Exception as exc:
                duration_ms = round((time.perf_counter() - start) * 1000, 1)
                logger.info(
                    "tool_call",
                    extra={"tool": tool_name, "duration_ms": duration_ms, "success": False, "error": str(exc)},
                )
                raise
            duration_ms = round((time.perf_counter() - start) * 1000, 1)
            logger.info("tool_call", extra={"tool": tool_name, "duration_ms": duration_ms, "success": True})
            return result

        return wrapper

    return decorator
