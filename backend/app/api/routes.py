"""Application API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_spam_keyword_service
from app.schemas.root import RootResponse
from app.schemas.spam_check import SpamCheckRequest, SpamCheckResponse
from app.schemas.spam_keyword import SpamKeywordCreate, SpamKeywordResponse
from app.services.root_service import get_root_message
from app.services.spam_check_service import check_spam
from app.services.spam_keyword_service import SpamKeywordService

router = APIRouter()


@router.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(message=get_root_message())


@router.post("/spam-check", response_model=SpamCheckResponse)
def spam_check(
    request: SpamCheckRequest,
    service: Annotated[SpamKeywordService, Depends(get_spam_keyword_service)],
) -> SpamCheckResponse:
    keywords = service.get_active_keywords()
    return check_spam(request.text, [item.keyword for item in keywords])


@router.get("/spam-keywords", response_model=list[SpamKeywordResponse])
def list_spam_keywords(
    service: Annotated[SpamKeywordService, Depends(get_spam_keyword_service)],
) -> list[SpamKeywordResponse]:
    return service.list_keywords()


@router.post(
    "/spam-keywords",
    response_model=SpamKeywordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_spam_keyword(
    request: SpamKeywordCreate,
    service: Annotated[SpamKeywordService, Depends(get_spam_keyword_service)],
) -> SpamKeywordResponse:
    return service.create_keyword(request)


@router.delete(
    "/spam-keywords/{keyword_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_spam_keyword(
    keyword_id: int,
    service: Annotated[SpamKeywordService, Depends(get_spam_keyword_service)],
) -> Response:
    if not service.delete_keyword(keyword_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keyword not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
