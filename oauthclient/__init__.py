import logging
from decouple import config
logger_name = config("LOGGER_NAME", default="ebay")
logger = logging.getLogger(config("LOGGER_NAME", default="ebay")).setLevel(config("LOG_LEVEL", default="INFO"))
# make the logger if it doesn't exist
if not logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(config("LOG_LEVEL", default="INFO"))
    logger.addHandler(logging.FileHandler(filename=logger_name + ".log"))
    logger.info("logger created")