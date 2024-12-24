"""
A skeleton of the file that needs to be implemented for each model endpoints.
Use this file only as a template
"""

import json
from typing import Dict, List, Union

from pyspark.sql.functions import col

from custom_logging import logger
from model_loader import light_pipeline, pretrained_pipeline, spark


def prepare_data(texts: List[str]):
    logger.debug("Preparing the Spark DataFrame")
    indexed_text = [(i, t) for i, t in enumerate(texts)]
    df = spark.createDataFrame(indexed_text, ["index", "text"])
    return df.repartition(1000)


def get_predictions_from_light_pipeline(texts: List[str]) -> Union[List[Dict], Dict]:
    logger.debug(f"Processing {len(texts)} texts with Light Pipeline")
    return light_pipeline.annotate(texts)


def get_predictions_from_pretrained_pipeline(
    texts: List[str],
) -> Union[List[Dict], Dict]:
    logger.debug(f"Processing {len(texts)} texts with Pretrained Pipeline")
    input_df = prepare_data(texts)
    predictions_df = pretrained_pipeline.transform(input_df)
    sorted_df = predictions_df.orderBy("index")
    logger.debug("Transformation complete, extracting results")

    ## Add logic that extracts required fields from the df

    output_df = sorted_df.select(
        col("finished_obfuscated").alias("obfuscated"),
        col("finished_masked").alias("masked"),
        col("finished_masked_with_chars").alias("masked_with_chars"),
        col("finished_masked_fixed_length_chars").alias("masked_fixed_length_chars"),
    )

    json_result = output_df.toJSON().collect()
    predictions_list = list(map(json.loads, json_result))

    return predictions_list


def get_predictions(texts: List[str]) -> Union[List[Dict], Dict]:
    if len(texts) < 20:
        return get_predictions_from_light_pipeline(texts)
    else:
        return get_predictions_from_pretrained_pipeline(texts)


def get_predictions_from_json_data(input_data: str) -> Dict:
    input_data_obj = json.loads(input_data)
    results = get_predictions(input_data_obj)
    consumed_units = len(results)

    return {
        "consumed_units": consumed_units,
        "predictions": results,
    }


def get_predictions_from_jsonlines_data(input_data: str) -> Dict:
    input_lines = input_data.splitlines()
    input_data_objs = []
    input_text = []

    for line in input_lines:
        record = json.loads(line)
        input_data_objs.append(record)
        input_text.append(input_data_objs)

    predictions = get_predictions(input_data_objs)
    return {"consumed_units": len(input_lines), "input_text": input_text, **predictions}


def get_json_response(predictions: List[str], **kwargs):
    return json.dumps({"predictions": predictions})


def get_jsonlines_response(predictions: List[str], **kwargs):
    return "\n".join([json.dumps({"predictions": pred}) for pred in predictions])


def get_predictions_for_snowflake(data: dict) -> Dict:
    input_texts = [i[1] for i in data["data"]]
    predictions = get_predictions(input_texts)
    return {"predictions": predictions}


def get_response_for_snowflake(predictions, **kwargs):
    return [[idx, prediction] for idx, prediction in enumerate(zip(predictions))]
