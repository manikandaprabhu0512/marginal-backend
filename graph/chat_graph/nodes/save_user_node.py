from db.crud import get_last_message, save_message
from graph.chat_graph.chat_state import ChatState
from helper.serializer import _message_to_dict
from telemetry.instrumentation import tracer


async def save_user_node(state: ChatState):

    with tracer.start_as_current_span("Save User Message"):
        if state["skip_save_user"]:
            user_message = await get_last_message(
                state["conversation_id"],
                role="user",
            )
        else:
            user_message = await save_message(
                state["conversation_id"],
                "user",
                state["message"],
            )

        return {
            "user_message": _message_to_dict(user_message),
        }