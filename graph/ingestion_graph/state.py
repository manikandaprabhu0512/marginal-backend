from typing import TypedDict


class GraphState(TypedDict):
    conversation_id: str
    query: str
    rewritten_query: str

    url_list: list[dict] | None