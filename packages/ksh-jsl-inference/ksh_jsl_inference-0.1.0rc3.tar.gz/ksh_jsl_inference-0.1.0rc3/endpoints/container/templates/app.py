from custom_logging import logger
from fastapi import FastAPI
from routers import healthcheck

logger.info("Starting FastAPI app")
app = FastAPI()

app.include_router(healthcheck.router)
