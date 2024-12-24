import logging
from typing import Dict, List


from endpoints.johnsnowlabs.encoder import AnnotationEncoder
from endpoints.container.base_inference_model import BaseInferenceModel
from endpoints.schema import Schema
import json

from pyspark.sql.dataframe import DataFrame


logger = logging.getLogger(__name__)


class MedicalNlpInferenceModel(BaseInferenceModel):

    def __init__(
        self,
    ):
        super().__init__(
            input=Schema(field="text", typing=str, required=True),
            input_params=[],
            output=Schema(field="predictions", typing=Dict),
        )
        self._spark = None
        self._light_pipeline = None

    @property
    def spark(self):
        if not self._spark:
            from .model_loader import spark, light_pipeline

            self._spark = spark
            self._light_pipeline = light_pipeline
        return self._spark

    @property
    def light_pipeline(self):
        if not self._light_pipeline:
            from .model_loader import spark, light_pipeline

            self._spark = spark
            self._light_pipeline = light_pipeline

        return self._light_pipeline

    def _prepare_data(self, texts: List[str]) -> DataFrame:
        logger.debug("Preparing the Spark DataFrame")
        indexed_text = [(i, t) for i, t in enumerate(texts)]
        df = self.spark.createDataFrame(indexed_text, ["index", "text"])
        return df.repartition(1000)

    def process_light_pipeline_results(
        self, inputs: List[str], results: List, params: Dict
    ):
        data = json.dumps(results, cls=AnnotationEncoder)
        return json.loads(data)

    def process_pretrained_pipeline_results(
        self, inputs: List[str], results: DataFrame, params: Dict
    ):
        json_result = results.toJSON().collect()
        return list(map(json.loads, json_result))

    def _get_predictions_from_light_pipeline(self, texts: List[str], params: Dict):
        logger.debug(f"Processing {len(texts)} texts with Light Pipeline")
        results = self.light_pipeline.fullAnnotate(texts)
        return self.process_light_pipeline_results(texts, results, params)

    def _get_predictions_from_pretrained_pipeline(
        self,
        texts: List[str],
        params: Dict,
    ):
        logger.debug(f"Processing {len(texts)} texts with Pretrained Pipeline")
        input_df = self._prepare_data(texts)
        predictions_df = self.light_pipeline.transform(input_df)
        sorted_df = predictions_df.orderBy("index")
        logger.debug("Transformation complete, extracting results")

        ## Add logic that extracts required fields from the df
        return self.process_pretrained_pipeline_results(texts, sorted_df, params)

    def concrete_predict(self, input_data: Dict) -> Dict:
        inputs = input_data["inputs"]
        params = input_data["params"]

        if isinstance(inputs, list) and len(inputs) >= 20:
            predictions = self._get_predictions_from_pretrained_pipeline(inputs, params)
        else:
            predictions = self._get_predictions_from_light_pipeline(inputs, params)

        return {self._output._field: predictions}
