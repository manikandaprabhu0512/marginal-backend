import json

from agents.confidence_agent import get_confidence_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async
from telemetry.instrumentation import tracer
from telemetry.metrics import llm_calls


async def confidence_node(state: ChatState):
    with tracer.start_as_current_span("Confidence"):
        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.CHECKING_CONFIDENCE,
                data={},
            )
        )

        with tracer.start_as_current_span("Confidence Agent"):
            confidence_agent = get_confidence_agent()

        input_payload = json.dumps(
            {
                "query": state["message"],
                "context": state["context"],
                "answer": state["answer"],
                "source": state["source"],
            }
        )

        with tracer.start_as_current_span("Generating confidence") as confidence_span:
            result = await retry_async(
                lambda: confidence_agent.ainvoke({"messages": [{"role": "user","content": input_payload}]})
            )

            llm_calls.add(1)

            ai_message = result["messages"][-1]
            metadata = ai_message.response_metadata
            usage = metadata["token_usage"]

            confidence_span.set_attribute("llm.provider", metadata["model_provider"])
            confidence_span.set_attribute("llm.model", metadata["model_name"])
            confidence_span.set_attribute("llm.service_tier", metadata["service_tier"])
            confidence_span.set_attribute("llm.input_tokens", usage["prompt_tokens"])
            confidence_span.set_attribute("llm.output_tokens", usage["completion_tokens"])
            confidence_span.set_attribute("llm.total_tokens", usage["total_tokens"])
            confidence_span.set_attribute(
                "llm.reasoning_tokens",
                usage["completion_tokens_details"]["reasoning_tokens"],
            )
            confidence_span.set_attribute("llm.finish_reason", metadata["finish_reason"])
            confidence_span.set_attribute("llm.request_id", metadata["id"])
            confidence_span.set_attribute("llm.run_id", ai_message.id)
            confidence_span.set_attribute("llm.agent", ai_message.name)

            confidence = parse_agent_json(result["messages"][-1].content)["confidence"]

            confidence_span.set_attribute("confidence", confidence)

            return {"confidence": confidence}