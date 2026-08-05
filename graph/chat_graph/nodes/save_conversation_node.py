from beanie import PydanticObjectId

from db.crud import save_turn
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def save_conversation_node(state: ChatState):

    with tracer.start_as_current_span("Save Assistant"):    
        answer = state["answer"]
        if state.get("source") == "general_knowledge":
            answer += (
                "\n\n"
                "*Note: This answer is based on general knowledge and not from your uploaded sources.*"
            )

        print("Saving Turn....")

        user_id_obj = PydanticObjectId(state["user_id"])
        await retry_async(
            lambda: save_turn(
                conversation_id=state["conversation_id"],
                user_id=user_id_obj,
                user={
                    "message": state["message"]
                },
                events=[],
                assistant={
                    "answer": answer,
                },
            )
        )

        print("Saved Turn....")

        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.ANSWER_READY,
                data={
                    "conversation_id": state["conversation_id"],
                    "user": state["message"],
                    "assistant": answer,
                    "confidence": state.get("confidence"),
                    "model_used": state.get("model_used"),
                    "source": state.get("source"),
                },
            )
        )

        return {
            "assistant_message": answer,
            "answer": answer,
        }