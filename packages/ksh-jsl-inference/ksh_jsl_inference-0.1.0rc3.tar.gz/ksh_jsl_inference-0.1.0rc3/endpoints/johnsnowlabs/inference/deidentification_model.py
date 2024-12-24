from typing import Dict, List
import json
from endpoints.johnsnowlabs.inference_model import MedicalNlpInferenceModel
from pyspark.sql.dataframe import DataFrame
from endpoints.schema import Schema
from pyspark.sql.functions import col
from endpoints.utils import get_attr_or_key


class DeidentificationModel(MedicalNlpInferenceModel):
    def __init__(self) -> None:
        super().__init__()
        self._input_params = [
            Schema(
                field="masking_policy",
                typing=str,
                required=False,
                dtypes=["masked", "obfuscated"],
                default="masked",
            ),
        ]
        self._output = Schema(field="predictions", typing=str)

    def _process_output(self, deid_res, text: str):
        sentences = deid_res["document"]
        obfuscateds = deid_res["obfuscated"]
        mask_entities = deid_res["mask_entity"]
        sentence_begin = 0
        obfuscated_str = ""
        masked_str = ""

        for index, sent in enumerate(sentences):
            begin = get_attr_or_key(sent, "begin")
            end = get_attr_or_key(sent, "end")
            obfuscated_result = get_attr_or_key(obfuscateds[index], "result")
            mask_entity_result = get_attr_or_key(mask_entities[index], "result")

            # Build the obfuscated and masked strings
            obfuscated_str += text[sentence_begin:begin] + obfuscated_result
            masked_str += text[sentence_begin:begin] + mask_entity_result
            sentence_begin = end + 1

        return {
            "masked": masked_str,
            "obfuscated": obfuscated_str,
        }

    def process_pretrained_pipeline_results(
        self, inputs: List[str], results: DataFrame, params: Dict
    ):
        output_df = results.select(
            col("document").alias("document"),
            col("mask_entity").alias("mask_entity"),
            col("obfuscated").alias("obfuscated"),
        )

        json_result = output_df.toJSON().collect()
        prediction_results = list(map(json.loads, json_result))
        return [
            self._process_output(res, text)[param["masking_policy"]]
            for res, text, param in zip(prediction_results, inputs, params)
        ]

    def process_light_pipeline_results(
        self, inputs: List[str], results: List, params: Dict
    ):

        return [
            self._process_output(res, text)[param["masking_policy"]]
            for res, text, param in zip(results, inputs, params)
        ]
