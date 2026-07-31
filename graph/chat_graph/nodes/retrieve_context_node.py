from config.redis_config import redis_config
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.retry import retry_async
from telemetry.instrumentation import tracer
from telemetry.logging import logger
from tools.retriever_tool import retrieve_context


async def retrieve_context_node(state: ChatState):
    print("Retrieve Context Called....")
    with tracer.start_as_current_span("Retrieve Context") as span:
        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.RETRIEVING_CONTEXT,
                data={},
            )
        )

        context = await retry_async(
            lambda: retrieve_context(state["conversation_id"], state["rewritten_query"], state["excluded_urls"])
        )

        span.set_attribute("query", len(state["rewritten_query"]))
        span.set_attribute("context.count", len(context))
        logger.info("Retrieved %s chunks", len(context))

        with open("context.txt", "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"Query: {state['rewritten_query']}\n\n")
            f.write(f"Length of Context: {len(context)}\n\n")
            f.write(context)
            f.write("\n")

        redis_config.set(state["conversation_id"], context)

        return {
            "context": context,
        }