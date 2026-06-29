from db.crud import save_message
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.retry import retry_async
from helper.serializer import _message_to_dict


async def save_assistant_node(state: ChatState):

    answer = state["answer"]

    if state.get("source") == "general_knowledge":
        answer += (
            "\n\n"
            "*Note: This answer is based on general knowledge and not from your uploaded sources.*"
        )

    assistant_message = await retry_async(
        lambda: save_message(
            conversation_id=state["conversation_id"],
            role="assistant",
            content=answer,
        )
    )

    await event_bus.publish(
        Event(
            conversation_id=state["conversation_id"],
            type=ChatEventType.ANSWER_READY,
            data={
                "conversation_id": state["conversation_id"],
                "user": state["user_message"],
                "assistant": _message_to_dict(assistant_message),
                "confidence": state.get("confidence"),
                "model_used": state.get("model_used"),
                "source": state.get("source"),
            },
        )
    )

    return {
        "assistant_message": _message_to_dict(assistant_message),
        "answer": answer,
    }