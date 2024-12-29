"""Setup and teardown functions."""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from rich import print as rprint
from .state import ApplicationState


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize an `ApplicationState` instance and attach it to `app.application_state`."""
    rprint("Starting up JupyterKernelServer")
    application_state = ApplicationState()
    app.state.application_state = application_state
    yield
    rprint("Tearing down any orphaned kernels.")
    await app.state.application_state.shutdown_kernels()
