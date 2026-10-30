"""FastAPI dependency providers."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.spam_keyword_repository import SpamKeywordRepository
from app.services.spam_keyword_service import SpamKeywordService


def get_spam_keyword_repository(
    session: Annotated[Session, Depends(get_db)],
) -> SpamKeywordRepository:
    return SpamKeywordRepository(session)


def get_spam_keyword_service(
    repository: Annotated[
        SpamKeywordRepository,
        Depends(get_spam_keyword_repository),
    ],
) -> SpamKeywordService:
    return SpamKeywordService(repository)
