from enum import Enum
from typing import TypedDict

from langchain_core.documents import Document


class WorkerStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class WorkerState(TypedDict):
    conversation_id: str

    url: dict

    page: Document | None

    page_result: dict | None

    status: WorkerStatus

    error: str | None