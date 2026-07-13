from langgraph.types import interrupt

from telemetry.instrumentation import tracer


def off_topic_decision_node(state):

    with tracer.start_as_current_span("Off Topic Decision") as span:    
        decision = interrupt(
            {
                "type": "off_topic",
                "message": "This question is outside the current notebook.",
                "topic": state["rewritten_query"],
                "actions": [
                    {
                        "id": "continue_general",
                        "label": "Continue with General Knowledge",
                    },
                    {
                        "id": "add_sources",
                        "label": "Add Sources to this Notebook",
                    },
                    {
                        "id": "create_notebook",
                        "label": "Create New Notebook",
                    },
                ],
            }
        )

        span.set_attribute("decision", decision)

        return {
            "decision": decision,
        }