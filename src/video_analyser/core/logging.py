"""Настройка логирования."""

import sys

from loguru import logger

from .config import settings


def setup_logging() -> None:
    """Настраивает loguru: вывод в консоль с уровнем из .env."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    )