import logging
from typing import Optional


def setup_logger(
    name: str = "config_manager", level: Optional[int] = None
) -> logging.Logger:
    """Set up the logger"""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if level is not None:
        logger.setLevel(level)

    return logger
