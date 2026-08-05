from typing import TypedDict

from beanie import PydanticObjectId


class GraphState(TypedDict):
    conversation_id: str
    query: str
    rewritten_query: str
    summary: str
    user_id: PydanticObjectId

    url_list: list[dict] | None

    events: list[dict] | None

    titles: list[str] | None