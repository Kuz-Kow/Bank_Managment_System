import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIRECTORY = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIRECTORY / "bank_management.log"
MAX_LOG_SIZE = 1_000_000
BACKUP_COUNT = 5


def configure_logging() -> None:
    """Configure an idempotent rotating file handler for application logs."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if any(
        handler.name == "bank_management_rotating_file"
        for handler in root_logger.handlers
    ):
        return

    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    file_handler.set_name("bank_management_rotating_file")
    root_logger.addHandler(file_handler)
