from db.crud import get_previous_turn
from graph.chat_graph.chat_state import ChatState
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def history_node(state: ChatState):
        print("History Fetched...")
        with tracer.start_as_current_span("Fetch History"):
            await event_bus.publish(
                Event(
                conversation_id=state["conversation_id"],
                type=ChatEventType.FETCHING_HISTORY,
                data={},
                )
            )

        history = await retry_async(
            lambda: get_previous_turn(state["conversation_id"])
        )

        print("History: ", history)
        if(history.user):
            print("user_message: ", history.user)
            print("user_message: ", history.user["message"])
        print("assistant_message: ", history.assistant["answer"])

        user_message = (
            history.user.get("message")
            if history and history.user
            else None
        )

        assistant_message = (
            history.assistant.get("answer")
            if history and history.assistant
            else None
        )

        return {
            "history": {
                "user": user_message,
                "assistant": assistant_message,
            },
        }
