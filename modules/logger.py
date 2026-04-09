import logging
import os

import colorlog


class WorkerIDFilter(logging.Filter):
    def __init__(self, show_pid: bool = False):
        super().__init__()
        self.show_pid = show_pid

    def filter(self, record: logging.LogRecord) -> bool:
        if self.show_pid:
            worker = os.getenv("UVICORN_WORKER")
            if worker:
                record.worker_id = f"-{worker}"
            else:
                record.worker_id = f"-{os.getpid()}"
        else:
            record.worker_id = ""
        return True


class CustomColoredFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        record.levelname_bracket = f"[{record.levelname}]"
        pad = 3 - len(record.levelname)
        record.levelname_pad = " " * pad if pad > 0 else ""
        return super().format(record)


def get_logger(name, show_time: bool = False, show_pid: bool = False):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        worker_filter = WorkerIDFilter(show_pid=show_pid)
        handler.addFilter(worker_filter)
        if show_time:
            formatter = CustomColoredFormatter(
                "[%(asctime)s] %(log_color)s[%(name)s%(worker_id)s]%(levelname_pad)s %(message)s%(reset)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "purple",
                    "CRITICAL": "red",
                },
                style="%",
            )
        else:
            formatter = CustomColoredFormatter(
                "%(log_color)s[%(name)s%(worker_id)s]%(levelname_pad)s %(message)s%(reset)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "purple",
                    "CRITICAL": "red",
                },
                style="%",
            )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    return logger
