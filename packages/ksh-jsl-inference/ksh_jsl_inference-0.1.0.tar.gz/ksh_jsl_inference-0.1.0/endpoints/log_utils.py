import logging

LOG_ROOT_NAME = "jsl_inference"

logger = logging.getLogger(LOG_ROOT_NAME)
logger.addHandler(logging.NullHandler())
