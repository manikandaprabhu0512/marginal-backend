from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from telemetry.instrumentation import tracer


async def context_analyzer(state: ChatState):
    with tracer.start_as_current_span("Context Analyzer") as span:
        context = state["context"]

        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.ANALYZING_CONTEXT,
                data={},
            )
        )


        if not context.strip():
            await event_bus.publish(
                Event(
                    conversation_id=state["conversation_id"],
                    type=ChatEventType.INSUFFICIENT_CONTEXT,
                    data={},
                )
            )

            span.set_attribute("insufficient", True)

            return {"insufficient": True}
        
        span.set_attribute("insufficient", False)
        
        return {"insufficient": False}