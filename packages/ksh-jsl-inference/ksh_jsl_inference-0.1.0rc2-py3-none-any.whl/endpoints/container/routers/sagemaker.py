import json
from http import HTTPStatus
from logging import getLogger

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from pydantic import ValidationError


router = APIRouter()


SUPPORTED_REQUEST_MIMETYPES = ["application/json", "application/jsonlines"]
SUPPORTED_RESPONSE_MIMETYPES = ["application/json", "application/jsonlines"]

logger = getLogger("prediction-service")


@router.post("/invocations")
async def invocations(request: Request):
    try:
        model = request.app.state.inference_model
        input_data = await request.body()
        content_type = request.headers.get("content-type", "application/json")
        accept = request.headers.get("accept", "application/json")

        if content_type not in SUPPORTED_REQUEST_MIMETYPES:
            raise HTTPException(
                status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                detail=f"Invalid Content-Type. Supported Content-Types: {', '.join(SUPPORTED_REQUEST_MIMETYPES)}",
            )
        response = None

        data = {}
        if content_type == "application/json":
            data = json.loads(input_data.decode("utf-8"))
        elif content_type == "application/jsonlines":
            input_lines = input_data.decode("utf-8").splitlines()
            data = []
            for line in input_lines:
                record = json.loads(line)
                data.append(record)
        predictions = model.predict(data)
        response_mimetype = (
            accept if accept in SUPPORTED_RESPONSE_MIMETYPES else content_type
        )
        if response_mimetype == "application/jsonlines":
            response = "\n".join(
                [
                    json.dumps({model._output._field: pred})
                    for pred in predictions[model._output._field]
                ]
            )
        elif response_mimetype == "application/json":
            response = json.dumps(predictions)
        return Response(
            content=response,
            media_type=response_mimetype,
        )
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
