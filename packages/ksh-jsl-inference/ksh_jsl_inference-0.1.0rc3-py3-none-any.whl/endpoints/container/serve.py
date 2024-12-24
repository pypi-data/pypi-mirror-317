import uvicorn
from logging import getLogger
from fastapi import FastAPI
from typing import Optional, Union

from endpoints.container.base_inference_model import BaseInferenceModel
from endpoints.johnsnowlabs.inference_model import MedicalNlpInferenceModel

from .routers import healthcheck

logger = getLogger("prediction_service")


def _create_fast_api_app(
    inferenceModel: Optional[BaseInferenceModel] = MedicalNlpInferenceModel(),
    include_sagemaker_route=False,
    include_snowflake_route=False,
):
    app = FastAPI()
    app.state.inference_model = inferenceModel

    app.include_router(healthcheck.router)
    if include_sagemaker_route:
        from .routers import sagemaker

        app.include_router(sagemaker.router)
    if include_snowflake_route:
        from .routers import snowflake

        app.include_router(snowflake.router)
    return app


def serve(
    sagemaker=False,
    snowflake=False,
    port=8080,
    inference_model: BaseInferenceModel = MedicalNlpInferenceModel(),
):
    app = _create_fast_api_app(
        inference_model,
        include_sagemaker_route=sagemaker,
        include_snowflake_route=snowflake,
    )
    uvicorn.run(app, host="0.0.0.0", port=port)
