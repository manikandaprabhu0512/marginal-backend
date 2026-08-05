from typing import TypedDict

from db.models import Message


class ChatState(TypedDict):
    conversation_id: str

    user_id: str

    message: str

    is_filler: bool

    query_type: str

    rewritten_query: str

    excluded_urls: list[str] | None

    skip_save_user: bool

    history: dict | None

    user_message: Message | None

    context: str | None

    query_intent: str | None

    insufficient : bool

    decision: str | None

    answer: str | None

    source: str | None

    confidence: float | None

    model_used: str | None

    assistant_message: Message | None

    response: dict