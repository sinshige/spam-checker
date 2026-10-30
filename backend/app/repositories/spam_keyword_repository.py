"""Database operations for spam keywords."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.spam_keyword import SpamKeyword


class SpamKeywordRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[SpamKeyword]:
        return list(
            self.session.scalars(
                select(SpamKeyword).order_by(SpamKeyword.id),
            ),
        )

    def list_active(self) -> list[SpamKeyword]:
        return list(
            self.session.scalars(
                select(SpamKeyword)
                .where(SpamKeyword.is_active.is_(True))
                .order_by(SpamKeyword.id),
            ),
        )

    def create(self, keyword: str, is_active: bool) -> SpamKeyword:
        spam_keyword = SpamKeyword(keyword=keyword, is_active=is_active)
        self.session.add(spam_keyword)
        self.session.commit()
        self.session.refresh(spam_keyword)
        return spam_keyword

    def delete(self, keyword_id: int) -> bool:
        spam_keyword = self.session.get(SpamKeyword, keyword_id)
        if spam_keyword is None:
            return False
        self.session.delete(spam_keyword)
        self.session.commit()
        return True
