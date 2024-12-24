import json
from http import HTTPStatus

import time
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from pydantic import ValidationError

from custom_logging import logger
from endpoint_logic import (
    get_json_response,
    get_jsonlines_response,
    get_predictions_from_json_data,
    get_predictions_from_jsonlines_data,
)

router = APIRouter()


SUPPORTED_REQUEST_MIMETYPES = ["application/json", "application/jsonlines"]
SUPPORTED_RESPONSE_MIMETYPES = ["application/json", "application/jsonlines"]


@router.post("/invocations")
async def invocations(request: Request):
    try:
        input_data = await request.body()
        content_type = request.headers.get("content-type", "application/json")
        accept = request.headers.get("accept", "application/json")

        if content_type not in SUPPORTED_REQUEST_MIMETYPES:
            raise HTTPException(
                status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                detail=f"Invalid Content-Type. Supported Content-Types: {', '.join(SUPPORTED_REQUEST_MIMETYPES)}",
            )
        model_response = {}
        response = None

        prediction_start_time = time.perf_counter()
        if content_type == "application/json":
            model_response = get_predictions_from_json_data(input_data.decode("utf-8"))
        elif content_type == "application/jsonlines":
            model_response = get_predictions_from_jsonlines_data(
                input_data.decode("utf-8")
            )
        logger.debug("Prediction time: %s", time.perf_counter() - prediction_start_time)

        response_mimetype = (
            accept if accept in SUPPORTED_RESPONSE_MIMETYPES else content_type
        )

        output_processing_time = time.perf_counter()
        if response_mimetype == "application/jsonlines":
            response = get_jsonlines_response(**model_response)
        elif response_mimetype == "application/json":
            response = get_json_response(**model_response)
        logger.debug(
            f"Output processing time: %s", time.perf_counter() - output_processing_time
        )

        return Response(
            content=response,
            media_type=response_mimetype,
            headers={
                "X-Amzn-Inference-Metering": json.dumps(
                    {
                        "Dimension": "inference.count",
                        "ConsumedUnits": model_response.get("consumed_units", 0),
                    }
                )
            },
        )
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
