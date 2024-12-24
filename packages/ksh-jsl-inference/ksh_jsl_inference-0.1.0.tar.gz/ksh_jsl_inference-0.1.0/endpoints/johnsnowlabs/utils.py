import os
import shutil

from johnsnowlabs import nlp
from sparknlp.pretrained import PretrainedPipeline
from endpoints.settings import MODEL_LOCATION


def download_healthcare_model(
    model_ref,
    language="en",
):

    try:
        os.makedirs("/opt/ml/", exist_ok=True)
        shutil.rmtree(MODEL_LOCATION, ignore_errors=True)
    except PermissionError:
        raise PermissionError(
            "Please make sure you have read/write permissions to /opt/ml/"
        )
    spark = nlp.start(model_cache_folder="model_cache")
    spark.sparkContext.setLogLevel("ERROR")

    if model_ref:
        # Cache model, if not specified user must
        # mount a folder to /app/model_cache/ which has a folder named `served_model`
        pretrained_pipeline = PretrainedPipeline(model_ref, language, "clinical/models")
        pretrained_pipeline.model.save(MODEL_LOCATION)
        shutil.rmtree("model_cache")
