"""Schemas for spam checking."""

from pydantic import BaseModel, ConfigDict, Field


class SpamCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str


class SpamCheckResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_spam: bool
    score: int = Field(ge=0, le=100)
    reason: str
