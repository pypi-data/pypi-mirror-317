"""Configure logging for library."""
import logging
from typing import Optional

from rich.logging import RichHandler

__all__ = [
    "set_up_logging",
]


def set_up_logging(logging_level: Optional[int] = None) -> None:
    """Configure logging."""
    if logging_level is None:
        logging_level = logging.INFO
    log_format = "%(message)s"
    logging.basicConfig(
        level=logging_level, format=log_format, datefmt="[%X]", handlers=[RichHandler()]
    )

    logging.debug("Logging set up successfully.")
