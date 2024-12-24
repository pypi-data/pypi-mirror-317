import json
import os
import time
from datetime import datetime
from http import HTTPStatus
from typing import Dict

from custom_logging import logger
from endpoint_logic import get_predictions_for_snowflake, get_response_for_snowflake
from fastapi import APIRouter, BackgroundTasks, Request, status
from fastapi.responses import JSONResponse, Response

# Environment variables below will be automatically populated by Snowflake.
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_HOST = os.getenv("SNOWFLAKE_HOST")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Custom environment variables
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")


BATCH_ID_STRING = "sf-external-function-query-batch-id"
SNOWFLAKE_BATCH_TABLE = "BATCH_JOBS"

router = APIRouter()


def get_login_token():
    with open("/snowflake/session/token", "r") as f:
        return f.read()


def get_connection_params() -> Dict:
    """
    Construct Snowflake connection params from environment variables.
    """
    if os.path.exists("/snowflake/session/token"):
        return {
            "account": SNOWFLAKE_ACCOUNT,
            "host": SNOWFLAKE_HOST,
            "authenticator": "oauth",
            "token": get_login_token(),
            "warehouse": SNOWFLAKE_WAREHOUSE,
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA,
        }
    else:
        return {
            "account": SNOWFLAKE_ACCOUNT,
            "user": SNOWFLAKE_USER,
            "password": SNOWFLAKE_PASSWORD,
            "role": SNOWFLAKE_ROLE,
            "warehouse": SNOWFLAKE_WAREHOUSE,
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA,
        }


def create_snowflake_session():
    from snowflake.snowpark import Session

    return Session.builder.configs(get_connection_params()).create()


def get_batch_results(batch_id: str):
    from snowflake.snowpark.functions import col

    with create_snowflake_session() as session:
        df = session.table(SNOWFLAKE_BATCH_TABLE).filter(col("BATCH_ID") == batch_id)
        result = df.first()
        if result:
            return (result["STATUS"], result["RESULTS"])
        else:
            return (None, None)


def store_batch_records(batch_id, data):
    from snowflake.snowpark.types import (
        IntegerType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )

    schema = StructType(
        [
            StructField("BATCH_ID", StringType()),
            StructField("CREATED_DATE", TimestampType()),
            StructField("NUMBER_OF_INPUTS", IntegerType()),
            StructField("RESULTS", StringType()),
            StructField("STATUS", StringType()),
        ]
    )

    with create_snowflake_session() as session:
        df = session.create_dataframe(
            [[batch_id, datetime.now(), len(data["data"]), "", "IN_PROGRESS"]], schema
        )
        df.write.mode("append").save_as_table(
            SNOWFLAKE_BATCH_TABLE, table_type="transient"
        )


def process_batch_input(batch_id, input_data):
    response_data = None
    status = "SUCCESS"
    try:
        logger.debug(f"Processing batch: {batch_id}")
        prediction_start_time = time.perf_counter()
        result = get_predictions_for_snowflake(input_data)
        logger.debug("Prediction time: %s", time.perf_counter() - prediction_start_time)

        logger.debug("Got predictions from background")
        output_processing_time = time.perf_counter()
        response_data = get_response_for_snowflake(**result)
        logger.debug(
            f"Output processing time: %s", time.perf_counter() - output_processing_time
        )
    except Exception as e:
        status = "ERROR"
        logger.error(e)
    with create_snowflake_session() as session:
        table = session.table(SNOWFLAKE_BATCH_TABLE)
        table.update(
            {"RESULTS": json.dumps({"data": response_data}), "STATUS": status},
            table["BATCH_ID"] == batch_id,
        )


@router.get("/invoke")
async def get_invoke_status(request: Request):
    batch_id = request.headers.get(BATCH_ID_STRING, "")
    logger.debug(f"Request status of Batch: {batch_id}")
    status_flag, result = get_batch_results(batch_id)
    if status_flag == "IN_PROGRESS":
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED, content={"message": "Processing"}
        )
    elif status_flag == "SUCCESS":
        return Response(
            status_code=status.HTTP_200_OK,
            content=result,
            media_type="application/json",
        )
    elif status_flag == "ERROR":
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Error processing request for batch: {batch_id}",
        )
    else:
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Unknown item status",
        )


@router.post("/invoke", status_code=status.HTTP_202_ACCEPTED)
async def invoke(request: Request, background_tasks: BackgroundTasks):
    try:
        batch_id = request.headers.get(BATCH_ID_STRING)
        data = await request.json()
        store_batch_records(batch_id, data)
        background_tasks.add_task(process_batch_input, batch_id, data)
        return {"message": "Processing"}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"detail": str(e)}
        )
