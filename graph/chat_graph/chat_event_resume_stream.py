import asyncio

from graph.chat_graph.chat_graph_service import resume_chat_graph
from graph.event_bus import event_bus
from graph.events.chat_events import ChatEventType
from helper.sse_event import sse_event


async def chat_event_resume_stream(
    conversation_id: str,
    decision: str
):
    resume_graph_task = asyncio.create_task(
        resume_chat_graph(conversation_id, decision)
    )

    async for event in event_bus.subscribe(conversation_id):
        yield sse_event(
            event.type.value,
            event.data,
        )

        if event.type in (
            ChatEventType.ANSWER_READY,
        ):
            break

    await resume_graph_task

    yield sse_event(
        "done",
        {},
    )