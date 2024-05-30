import logging
import os
from logging import Logger

if os.path.isfile(os.path.join("src/src.logger.txt")):
    os.remove(os.path.join("src/src.logger.txt"))


def logger_setup() -> Logger:
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("logger.txt", mode="w")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    return logger
