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

def setup_logger(name: str, log_file: Path = None, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Only add handlers if none exist
    if not logger.handlers:
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # File handler
        if log_file is None:
            log_file = LOG_DIR / f"{name}.log"
        fh = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
        )
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
