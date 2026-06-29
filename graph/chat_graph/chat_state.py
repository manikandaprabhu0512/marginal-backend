from typing import TypedDict

from db.models import Message


class ChatState(TypedDict):
    conversation_id: str

    message: str

    query_type: str

    rewritten_query: str

    excluded_urls: list[str] | None

    skip_save_user: bool

    history: list

    user_message: Message | None

    context: str

    answer: str | None

    source: str | None

    confidence: float | None

    model_used: str | None

    assistant_message: Message | None

    response: dict