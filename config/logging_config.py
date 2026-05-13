import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Log directory
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Logger configuration
def setup_logger(name: str = "agrocontrol") -> logging.Logger:
    """Logger sozlash"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Agar handler allaqachon qo'shilgan bo'lsa, qayta qo'shmaslik
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        LOG_DIR / "agrocontrol.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)

    # Error file handler
    error_handler = RotatingFileHandler(
        LOG_DIR / "errors.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger


# Global logger
logger = setup_logger()
