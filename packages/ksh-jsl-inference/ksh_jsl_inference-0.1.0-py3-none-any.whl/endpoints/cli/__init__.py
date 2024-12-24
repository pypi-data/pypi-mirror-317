from .cli import cli
from .sagemaker.commands import sagemaker
from .snowflake.commands import snowflake

import logging

# Configure logging for the cli app
logging.basicConfig(level=logging.INFO)
