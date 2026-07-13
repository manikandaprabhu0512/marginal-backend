import json

from agents.query_understanding_agent import get_query_understanding_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async
from telemetry.instrumentation import tracer
from telemetry.logging import logger
from telemetry.metrics import llm_calls


async def query_understanding_node(state: ChatState):
    with tracer.start_as_current_span("Query Understanding") as span:
        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.UNDERSTANDING_QUERY,
                data={},
            )
        )

        understanding_agent = get_query_understanding_agent()

        query_payload = json.dumps({"query": state["message"], "history": state["history"]})

        result = await retry_async(
            lambda: understanding_agent.ainvoke(
                {"messages": [{"role": "user", "content": query_payload}]}
            )
        )

        llm_calls.add(1)

        ai_message = result["messages"][-1]
        metadata = ai_message.response_metadata
        usage = metadata["token_usage"]

        span.set_attribute("llm.provider",metadata["model_provider"])
        span.set_attribute("llm.model",metadata["model_name"])
        span.set_attribute("llm.input_tokens",usage["prompt_tokens"])
        span.set_attribute("llm.output_tokens",usage["completion_tokens"])
        span.set_attribute("llm.total_tokens",usage["total_tokens"])
        span.set_attribute("llm.reasoning_tokens",usage["completion_tokens_details"]["reasoning_tokens"])
        span.set_attribute("llm.prompt_time",usage["prompt_time"])
        span.set_attribute("llm.completion_time",usage["completion_time"])
        span.set_attribute("llm.queue_time",usage["queue_time"])
        span.set_attribute("llm.total_time",usage["total_time"])
        span.set_attribute("llm.finish_reason",metadata["finish_reason"])
        span.set_attribute("llm.service_tier",metadata["service_tier"])

        data = parse_agent_json(result["messages"][-1].content)

        span.set_attribute("query_type", data["type"])

        logger.info("Query Type: %s", data["type"])

        return {
            "query_type": data["type"],
            "rewritten_query": data["rewritten_query"],
            "answer": data["direct_answer"]
        }