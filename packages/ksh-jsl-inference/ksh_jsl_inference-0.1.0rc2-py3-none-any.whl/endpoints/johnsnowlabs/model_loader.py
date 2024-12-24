import multiprocessing
import os
import sys

from johnsnowlabs import nlp
from sparknlp.pretrained import LightPipeline, PretrainedPipeline

os.environ["PYSPARK_PYTHON"] = sys.executable
import logging

os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


logger = logging.getLogger(__name__)
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
                logger.error(
                    f"Error loading model: {e}. Please make sure you have downloaded the model and placed it on /opt/ml/model"
                )
                raise
        return cls._model, LightPipeline(cls._model.model)


logger.debug(f"vCPU Count: {multiprocessing.cpu_count()}")
pretrained_pipeline, light_pipeline = ModelLoader.load_model()
