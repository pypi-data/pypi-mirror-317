"""Pydantic Models for the juptyer_client library.

These models follow the specification laid out in: [Jupyter's documentation][1]

[1]: https://jupyter-client.readthedocs.io/en/latest/messaging.html#general-message-format
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum, auto
from typing import Optional

from pydantic import BaseModel, validator

# Schema for interacting with jupyter kernels via `jupyter_client`
#
#
#


class MessageType(StrEnum):
    """Different message types."""

    EXECUTE_INPUT = auto()
    STATUS = auto()
    OTHER = "other"


class MessageHeader(BaseModel):
    """Pydantic Model for Jupyter message headers."""

    msg_id: str
    session: str
    username: str
    date: datetime
    msg_type: MessageType
    version: str
    subshell_id: Optional[str] = None

    @validator("msg_type", pre=True)
    def validate_msg_type(cls, v):
        """Validate that the msg_type returned by the kernel is defined in our enum."""
        try:
            return MessageType(v)
        except ValueError:
            # print("[[[]]] Received new message type: {}".format(v))
            return MessageType.OTHER


class Message(BaseModel):
    """A high-level representation of messages sent along the wire."""

    header: MessageHeader
    msg_id: str
    msg_type: str
    parent_header: dict
    content: dict
    metadata: dict
    buffers: list


# Schema for representing different components of a jupyter notebook
#
#


class JupyterNotebook(BaseModel):
    """Pydantic model of a complete jupyter notebook ()."""

    metadata: NotebookMetadata = None
    nbformat: int
    nbformat_minor: int
    cells: list[NotebookCell] = []


class NotebookMetadata(BaseModel):
    """Pydantic Model containing metadata about a notebook."""

    kernel_info: Optional[KernelInfo] = None
    language_info: Optional[LanguageInfo] = None


class KernelInfo(BaseModel):
    """Model used to store information about the kernel used."""

    name: str


class LanguageInfo(BaseModel):
    """Model used to store information about the language used inside the notebook."""

    name: str
    version: str
    codemirror_mode: Optional[str] = None


class NotebookCell(BaseModel):
    """Pydantic Model for notebook cells."""
