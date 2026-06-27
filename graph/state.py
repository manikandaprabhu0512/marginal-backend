from typing import TypedDict


class GraphState(TypedDict):
    conversation_id: str
    query: str

    url_list: list[dict]