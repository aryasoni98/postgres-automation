import logging
import sys
from pathlib import Path
from loguru import logger
from api.config.settings import settings

def setup_logging():
    logger.remove()

    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG" if settings.DEBUG else "INFO",
        backtrace=True,
        diagnose=True,
    )

    log_file = Path("logs/api.log")
    log_file.parent.mkdir(exist_ok=True)
    logger.add(
        log_file,
        rotation="500 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        backtrace=True,
        diagnose=True,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        ) 