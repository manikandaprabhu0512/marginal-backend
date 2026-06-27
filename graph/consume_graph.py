from graph.graph import graph
from helper.event_bus import Event, EventType, event_bus


async def consume_graph(conversation_id: str, query: str):
    print("Called Consume_graph...")

    async for _ in graph.astream(
        {"conversation_id": conversation_id,"query": query}
    ):
        pass

    await event_bus.publish(
        Event(
            conversation_id=conversation_id,
            type=EventType.INGESTION_COMPLETED,
            data={}
        )
    )