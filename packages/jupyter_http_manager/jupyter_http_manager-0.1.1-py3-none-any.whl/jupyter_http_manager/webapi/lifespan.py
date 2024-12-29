"""Setup and teardown functions."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .logger import logger
from .state import ApplicationState


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize an `ApplicationState` instance and attach it to `app.application_state`."""
    application_state = ApplicationState()
    app.state.application_state = application_state
    yield
    logger.info("Shutting down managed kernels.")
    await app.state.application_state.shutdown_kernels()
