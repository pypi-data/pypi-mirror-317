import multiprocessing
import os
import sys

from johnsnowlabs import nlp
from sparknlp.pretrained import LightPipeline, PretrainedPipeline

from custom_logging import logger

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


logger.info("Starting spark session")

spark = nlp.start()
spark.sparkContext.setLogLevel("ERROR")

logger.info("Spark session started")


class ModelLoader:
    _model = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            try:
                logger.info("Loading model from /opt/ml/model")
                cls._model = PretrainedPipeline.from_disk("/opt/ml/model")
                logger.info("Model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise
        return cls._model, LightPipeline(cls._model.model)


logger.debug(f"vCPU Count: {multiprocessing.cpu_count()}")
pretrained_pipeline, light_pipeline = ModelLoader.load_model()
