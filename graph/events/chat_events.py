from enum import Enum


class ChatEventType(str, Enum):
    FETCHING_HISTORY = "fetching_history"
    UNDERSTANDING_QUERY = "understanding_query"
    GENERATING_ANSWER = "generating_answer"
    RETRIEVING_CONTEXT = "retrieving_context"

    SMALLER_MODEL_GENERATING_ANSWER = "smaller_model_generating_answer"
    CHECKING_CONFIDENCE = "checking_confidence"
    LARGER_MODEL_GENERATING_ANSWER = "larger_model_generating_answer"

    ANSWER_READY = "answer_ready"