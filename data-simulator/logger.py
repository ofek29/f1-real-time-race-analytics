import logging
import os


def setup_logger():
    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=log_level, format=log_format, handlers=[logging.StreamHandler()]
    )

    logger = logging.getLogger("dataSimLogger")
    return logger


logger = setup_logger()
