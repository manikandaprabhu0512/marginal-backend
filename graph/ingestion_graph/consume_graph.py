from beanie import PydanticObjectId

from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.ingestion_graph import graph


async def consume_graph(conversation_id: str, query: str, user_id: PydanticObjectId):

    async for _ in graph.astream(
        {"conversation_id": conversation_id,"query": query, "user_id" : user_id}
    ):
        pass

    await event_bus.publish(
        Event(
            conversation_id=conversation_id,
            type=IngestionEventType.INGESTION_COMPLETED,
            data={}
        )
    )