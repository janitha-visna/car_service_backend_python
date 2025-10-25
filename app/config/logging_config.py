import logging
import logging.handlers
from pathlib import Path

# Directory to store logs
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# File path for logs
LOG_FILE = LOG_DIR / "app.log"

# Log format for readability
LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
)

def setup_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up and returns a configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # === Handlers ===
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # === Formatter ===
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # === Attach handlers ===
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
