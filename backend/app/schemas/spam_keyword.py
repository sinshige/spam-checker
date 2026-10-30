"""Schemas for spam keyword management."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SpamKeywordCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    keyword: str = Field(min_length=1, max_length=255)
    is_active: bool = True


class SpamKeywordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    keyword: str
    is_active: bool
    created_at: datetime
