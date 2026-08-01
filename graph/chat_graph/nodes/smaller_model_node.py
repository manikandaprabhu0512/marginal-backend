import json

from agents.smaller_model_agent import get_smaller_model_agent
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.json_parser import parse_agent_json
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def smaller_model_node(state: ChatState):

    with tracer.start_as_current_span("Smaller Model") as span:
        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.SMALLER_MODEL_GENERATING_ANSWER,
                data={},
            )
        )

        with tracer.start_as_current_span("Smaller Agent"):
            smaller_agent = await get_smaller_model_agent(state["conversation_id"])

        input_payload = json.dumps(
            {
                "query": state["message"],
                "context": state["context"],
                "history": state["history"],
            }
        )

        with tracer.start_as_current_span("Generating answer") as smaller_span:
            result = await retry_async(
                lambda: smaller_agent.ainvoke(
                    {"messages": [{"role": "user","content": input_payload}]}
                )
            )

            ai_message = result["messages"][-1]
            metadata = ai_message.response_metadata
            usage = metadata["token_usage"]

            smaller_span.set_attribute("llm.provider", metadata["model_provider"])
            smaller_span.set_attribute("llm.model", metadata["model_name"])
            smaller_span.set_attribute("llm.service_tier", metadata["service_tier"])
            smaller_span.set_attribute("llm.input_tokens", usage["prompt_tokens"])
            smaller_span.set_attribute("llm.output_tokens", usage["completion_tokens"])
            smaller_span.set_attribute("llm.total_tokens", usage["total_tokens"])
            smaller_span.set_attribute(
                "llm.reasoning_tokens",
                usage["completion_tokens_details"]["reasoning_tokens"],
            )
            smaller_span.set_attribute("llm.finish_reason", metadata["finish_reason"])
            smaller_span.set_attribute("llm.request_id", metadata["id"])
            smaller_span.set_attribute("llm.run_id", ai_message.id)
            smaller_span.set_attribute("llm.agent", ai_message.name)

            data = parse_agent_json(result["messages"][-1].content)

            span.set_attribute("source", data["source"])

            return {
                "answer": data["answer"],
                "source": data["source"],
                "model_used": "smaller_model",
            }