"""Pydantic Models used to receive data."""

from pydantic import BaseModel


class Kernel(BaseModel):
    """Model used to capture the name of a given kernel."""

    name: str = "python3"


class ExecutionRequest(BaseModel):
    """Request to execute a block of code."""

    kernel_name: str = "python3"
    source_code: str = "10 + 10"
