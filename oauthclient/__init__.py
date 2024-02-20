import logging
from decouple import config
logger_name = config("LOGGER_NAME", default="ebay")
log_level = config("LOG_LEVEL", default="INFO")
logger = logging.getLogger(logger_name)
logger.setLevel(log_level)
if not logger.hasHandlers():
    logger.addHandler(logging.FileHandler(filename=logger_name + ".log"))
logger.info("ebay oauth logger connected")