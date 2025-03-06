import logging
import os


def setup_logger():
    logger = logging.getLogger("dataSimLogger")

    # Only configure the logger if it doesn't already have handlers
    if not logger.handlers:
        log_level = os.getenv("LOG_LEVEL", "DEBUG")
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        logger.setLevel(log_level)
        logger.addHandler(handler)

    return logger


logger = setup_logger()
