import uvicorn
import os
from fastapi import FastAPI
from typing import Optional
import logging

from endpoints.container.base_inference_model import BaseInferenceModel
from endpoints.johnsnowlabs.inference_model import MedicalNlpInferenceModel

from .routers import healthcheck


def _configure_logging():
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level)


def _create_fast_api_app(
    inferenceModel: Optional[BaseInferenceModel] = MedicalNlpInferenceModel(),
    include_sagemaker_route=False,
    include_snowflake_route=False,
):
    app = FastAPI()
    _configure_logging()
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
    if isinstance(inference_model, BaseInferenceModel):
        # Preload the spark and light_pipeline during the initialization
        from endpoints.johnsnowlabs.model_loader import spark, light_pipeline

    app = _create_fast_api_app(
        inference_model,
        include_sagemaker_route=sagemaker,
        include_snowflake_route=snowflake,
    )
    uvicorn.run(app, host="0.0.0.0", port=port)
