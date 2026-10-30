"""Schemas for the root endpoint."""

from pydantic import BaseModel, ConfigDict


class RootResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
