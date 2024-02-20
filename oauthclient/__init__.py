import logging
from decouple import config
logger = logging.getLogger(config("LOGGER_NAME", default="ebay")).setLevel(config("LOG_LEVEL", default="INFO"))