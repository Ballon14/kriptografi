"""
Logging configuration module.
"""


import logging

from logging.handlers import RotatingFileHandler

from config import LOG_DIR


LOG_FILE = LOG_DIR / "secure_file_vault.log"



def setup_logger() -> logging.Logger:
    """
    Configure application logger.
    """

    logger = logging.getLogger(
        "SecureFileVault"
    )

    logger.setLevel(
        logging.INFO
    )


    if not logger.handlers:

        handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )


        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )


        handler.setFormatter(
            formatter
        )


        logger.addHandler(
            handler
        )


    return logger
