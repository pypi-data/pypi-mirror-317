import logging
import os
import sys


# Logger configuration
def get_logger(logger_name):
    log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(
        logging.Formatter("%(name)s [%(asctime)s] [%(levelname)s] %(message)s")
    )
    logger.addHandler(handler)
    return logger


logger = get_logger("prediction-service")
