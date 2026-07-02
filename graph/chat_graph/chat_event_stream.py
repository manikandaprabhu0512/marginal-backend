import asyncio

from graph.chat_graph.consume_chat_graph import consume_chat_graph
from graph.event_bus import event_bus
from graph.events.chat_events import ChatEventType
from helper.sse_event import sse_event


async def chat_event_stream(
    conversation_id: str,
    message: str,
    excluded_urls: list[str] | None = None,
    skip_save_user: bool = False,
):
    graph_task = asyncio.create_task(
        consume_chat_graph(
            conversation_id=conversation_id,
            message=message,
            excluded_urls=excluded_urls,
            skip_save_user=skip_save_user,
        )
    )

    async for event in event_bus.subscribe(conversation_id):
        yield sse_event(
            event.type.value,
            event.data,
        )

        if event.type in (
            ChatEventType.ANSWER_READY,
            ChatEventType.INTERRUPTED,
            ChatEventType.CREATED_NOTEBOOK
        ):
            break

    await graph_task

    yield sse_event(
        "done",
        {},
    )