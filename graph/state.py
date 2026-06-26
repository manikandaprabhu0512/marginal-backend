from beanie import Document
from typing_extensions import TypedDict


class GraphState(TypedDict):
    conversation_id: str
    query: str

    url_list: list[str]
    pages: list[Document]
    page_results: list[dict]