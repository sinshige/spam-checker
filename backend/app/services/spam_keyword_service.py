"""Spam keyword use cases."""

from app.repositories.spam_keyword_repository import SpamKeywordRepository
from app.schemas.spam_keyword import SpamKeywordCreate, SpamKeywordResponse


class SpamKeywordService:
    def __init__(self, repository: SpamKeywordRepository) -> None:
        self.repository = repository

    def list_keywords(self) -> list[SpamKeywordResponse]:
        return [
            SpamKeywordResponse.model_validate(item)
            for item in self.repository.list_all()
        ]

    def get_active_keywords(self) -> list[SpamKeywordResponse]:
        return [
            SpamKeywordResponse.model_validate(item)
            for item in self.repository.list_active()
        ]

    def create_keyword(self, request: SpamKeywordCreate) -> SpamKeywordResponse:
        item = self.repository.create(request.keyword, request.is_active)
        return SpamKeywordResponse.model_validate(item)

    def delete_keyword(self, keyword_id: int) -> bool:
        return self.repository.delete(keyword_id)
