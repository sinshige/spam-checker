"""Rule-based spam detection."""

import re

from app.schemas.spam_check import SpamCheckResponse

URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
RULE_SCORES = {"url": 90, "email": 80, "ng_word": 70}


def check_spam(text: str, ng_words: list[str]) -> SpamCheckResponse:
    """Classify text using URL, email address, and prohibited-word rules."""
    reasons: list[str] = []
    score = 0

    if URL_PATTERN.search(text):
        score += RULE_SCORES["url"]
        reasons.append("URLを含むため")

    if EMAIL_PATTERN.search(text):
        score += RULE_SCORES["email"]
        reasons.append("メールアドレスを含むため")

    matched_words = [word for word in ng_words if word in text]
    if matched_words:
        score += RULE_SCORES["ng_word"]
        reasons.append(f"NGワード「{'、'.join(matched_words)}」を含むため")

    if not reasons:
        return SpamCheckResponse(
            is_spam=False,
            score=0,
            reason="該当するルールはありません",
        )

    return SpamCheckResponse(
        is_spam=True,
        score=min(score, 100),
        reason="、".join(reasons),
    )
