CONFIDENCE_THRESHOLD = 0.75

def router_after_context_analyzer(state):

    if state["insufficient"] is True:
        return "off_topic_decision"

    return "smaller_model"

def route_after_query_understanding(state):

    match state["query_type"]:

        case "question":
            return "retrieve_context"

        case "filler":
            return "save_user"

        case "off_topic":
            return "off_topic_decision"

        case _:
            raise ValueError(f"Unknown query type: {state['query_type']}")


def route_after_off_topic_decision(state):

    match state["decision"]:

        case "continue_general":
            return "general_knowledge"
        
        case "add_sources":
            return "add_sources"
        
        case "create_notebook":
            return "create_notebook"

        case _:
            raise ValueError(f"Unknown decision: {state['decision']}")


def route_after_smaller_model(state):

    if state["source"] == "general_knowledge":
        return "save_user"

    return "confidence"


def route_after_confidence(state):

    if state["confidence"] >= CONFIDENCE_THRESHOLD:
        return "save_user"

    return "larger_model"