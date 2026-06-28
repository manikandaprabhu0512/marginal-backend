CONFIDENCE_THRESHOLD = 0.75


def route_after_smaller_model(state):

    if state["source"] == "general_knowledge":
        return "save_assistant"

    return "confidence"


def route_after_confidence(state):

    if state["confidence"] >= CONFIDENCE_THRESHOLD:
        return "save_assistant"

    return "larger_model"