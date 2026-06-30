from background.cleanup_checkpoint import cleanup_checkpoints
from background.manager import background_manager
from graph.chat_graph.chat_graph import chat_graph
from graph.event_bus import Event, event_bus
from graph.events.chat_events import ChatEventType


async def consume_chat_graph(
    conversation_id: str,
    message: str,
    excluded_urls: list[str] | None = None,
    skip_save_user: bool = False,
):
    config = {
        "configurable": {
            "thread_id": conversation_id,
        }
    }

    async for event in chat_graph.astream(
        {
            "conversation_id": conversation_id,
            "message": message,
            "excluded_urls": excluded_urls,
            "skip_save_user": skip_save_user,
            "confidence": None,
        },
        config=config,
    ):
        if "__interrupt__" in event:
            await event_bus.publish(
                Event(
                    conversation_id=conversation_id,
                    type=ChatEventType.INTERRUPTED,
                    data=event["__interrupt__"][0].value,
                )
            )
            return
        
    background_manager.submit(
        cleanup_checkpoints(conversation_id)
    )