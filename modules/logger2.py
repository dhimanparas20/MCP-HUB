import os
import sys
from typing import Optional

import loguru


def _get_format(
    show_time: bool = False, show_pid: bool = False, log_name: str = ""
) -> str:
    parts = []

    if show_time:
        parts.append("{time:YYYY-MM-DD HH:mm:ss}")

    if show_pid:
        parts.append(f"{log_name}{{extra[pid]}}")
    else:
        parts.append(log_name)

    parts.append("{level: <8}")

    parts.append("{message}")

    return " | ".join(parts)


def get_logger(
    name: str,
    show_time: bool = False,
    show_pid: bool = False,
    color: bool = True,
):
    log_name = f"[{name}]"
    log_format = _get_format(show_time, show_pid, log_name)

    loguru.logger.remove()

    if show_pid:
        worker = os.getenv("UVICORN_WORKER")
        pid_str = f"-{worker}" if worker else f"-{os.getpid()}"
    else:
        pid_str = ""

    loguru.logger.add(
        sys.stderr,
        format=log_format,
        level="DEBUG",
        colorize=color,
        backtrace=True,
        diagnose=True,
    )

    return loguru.logger.bind(pid=pid_str)


def add_file_handler(
    log_path: str,
    rotation: str = "10 MB",
    retention: str = "7 days",
    level: str = "INFO",
) -> None:
    loguru.logger.add(
        log_path,
        rotation=rotation,
        retention=retention,
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {name} | {level: <8} | {message}",
        backtrace=True,
        diagnose=True,
    )
