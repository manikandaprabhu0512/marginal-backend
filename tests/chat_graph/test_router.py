import pytest

from graph.chat_graph.nodes.router import (route_after_confidence,
                                           route_after_off_topic_decision,
                                           route_after_query_understanding,
                                           route_after_smaller_model,
                                           router_after_context_analyzer)

# ======================== query_understanding ========================

# def test_question_routes_to_retrieve_context():

#     state = {
#         "query_type": "question"
#     }

#     assert route_after_query_understanding(state) == "retrieve_context"

# def test_filler_routes_to_save_assistant():

#     state = {
#         "query_type": "filler"
#     }

#     assert route_after_query_understanding(state) == "save_assistant"

# def test_off_topic_routes_to_off_topic_decision():

#     state = {
#         "query_type": "off_topic"
#     }

#     assert route_after_query_understanding(state) == "off_topic_decision"


@pytest.mark.parametrize(
    "query_type, expected",
    [
        ("question", "retrieve_context"),
        ("filler", "save_assistant"),
        ("off_topic", "off_topic_decision"),
    ]
)
def test_route_after_query_understanding(query_type, expected):

    state = {
        "query_type": query_type
    }

    assert route_after_query_understanding(state) == expected
    
def test_unknown_query_type():

    state = {
        "query_type": "hello"
    }

    with pytest.raises(ValueError,match="Unknown query type"):
        route_after_query_understanding(state)

# ======================== context_analyzer ========================

@pytest.mark.parametrize(
    "insufficient, expected",
    [
        (False, "smaller_model"),
        (True, "off_topic_decision")
    ]
)
def test_router_after_context_analyzer(insufficient, expected):

    state = {
        "insufficient": insufficient
    }

    assert router_after_context_analyzer(state) == expected

# ======================== confidence ========================

@pytest.mark.parametrize(
    "confidence, expected",
    [
        (0.90, "save_assistant"),
        (0.50, "larger_model"),
        (0.75, "save_assistant"),
    ],
)
def test_route_after_confidence(confidence, expected):

    state = {
        "confidence" : confidence
    }

    assert route_after_confidence(state) == expected

# ======================== smaller_model ========================

@pytest.mark.parametrize(
    "source, expected",
    [
        ("general_knowledge", "save_assistant"),
        ("knowledge_base", "confidence"),
    ],
)
def test_route_after_smaller_model(source, expected):

    state = {
        "source" : source
    }

    assert route_after_smaller_model(state) == expected

# ======================== off_topic_decision ========================

@pytest.mark.parametrize(
    "decision, expected",
    [
        ("continue_general", "general_knowledge"),
        ("add_sources", "add_sources"),
        ("create_notebook", "create_notebook"),
    ],
)
def test_route_after_off_topic_decision(decision, expected):

    state = {
        "decision" : decision
    }

    assert route_after_off_topic_decision(state) == expected

def test_unknown_off_topic_decision():

    state = {
        "decision": "skip"
    }

    with pytest.raises(ValueError, match="Unknown decision"):
        route_after_off_topic_decision(state)