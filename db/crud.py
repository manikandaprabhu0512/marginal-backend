from datetime import datetime, timezone

from beanie import PydanticObjectId

from db.models import Conversation, Message, ScrapedURLs, Source
from helper.file_type import detect_source_type
from tools.vectorize_tool import delete_vectorize


async def get_or_create_conversation(conversation_id: str, title: str = None) -> Conversation:
    conv = await Conversation.find_one(Conversation.conversation_id == conversation_id)
    if not conv:
        conv = Conversation(
            conversation_id=conversation_id,
            title=title or "Untitled Notebook"
        )
        await conv.insert()
    return conv


async def db_get_conversation(conversation_id: str):
    conv = await Conversation.find_one(Conversation.conversation_id == conversation_id)
    if not conv:
        raise ValueError(f"Conversation {conversation_id} not found")
    return conv


async def update_conversation_activity(conversation_id: str):
    conv = await Conversation.find_one(Conversation.conversation_id == conversation_id)
    if not conv:
        raise ValueError(f"Conversation {conversation_id} not found")    
    conv.last_activity = datetime.now(timezone.utc)
    await conv.save()


async def update_conversation_title(conversation_id: str, title: str):
    conv = await Conversation.find_one(Conversation.conversation_id == conversation_id)
    if not conv:
        raise ValueError(f"Conversation {conversation_id} not found")
    conv.title = title
    conv.last_activity = datetime.now(timezone.utc)
    await conv.save()
    return conv


async def list_conversations() -> list[dict]:
    conversations = await Conversation.find_all().sort("-last_activity").limit(3).to_list()
    return [
        {
            "conversation_id": c.conversation_id,
            "title": c.title,
            "created_at": c.created_at,
            "last_activity": c.last_activity,
            "source_count": c.source_count,
        }
        for c in conversations
    ]


async def get_history(conversation_id: str) -> list[dict]:
    messages = await (
        Message.find(Message.conversation_id == conversation_id)
        .sort("+created_at")
        .to_list()
    )
    return [{"role": m.role, "content": m.content} for m in messages]


async def save_message(conversation_id: str, role: str, content: str):
    message = await Message(conversation_id=conversation_id, role=role, content=content).insert()
    await update_conversation_activity(conversation_id)
    return message


async def save_sources(conversation_id: str, sources: list[dict]):
    docs = [
        Source(conversation_id=conversation_id, url=s["url"], title=s["title"], source_type=s["source_type"], vector_ids=s["vector_ids"])
        for s in sources
    ]
    if docs:
        await Source.insert_many(docs) 
        count = await Source.find(Source.conversation_id == conversation_id).count()
        await update_source_count(conversation_id, count)

async def save_source(conversation_id: str,source: dict):
    await Source(
        conversation_id=conversation_id,
        title=source["title"],
        url=source["url"],
        source_type=detect_source_type(source["url"]),
        vector_ids=source.get("vector_ids", []),
    ).insert()

    count = await Source.find(Source.conversation_id == conversation_id).count()
    await update_source_count(conversation_id, count)

async def get_sources(conversation_id: str) -> list[dict]:
    sources = await Source.find(Source.conversation_id == conversation_id).to_list()   
    return sources
    # return [{"id": str(s.id), "url": s.url, "title": s.title, "source_type": s.source_type, "vector_ids": s.get("vector_ids") or []} for s in sources]

async def get_source(source_id: PydanticObjectId):
    return await Source.find_one(Source.id == source_id)

async def get_messages(conversation_id: str) -> list[dict]:
    messages = await (
        Message.find(Message.conversation_id == conversation_id)
        .sort("+created_at")
        .to_list()
    )
    return [
        {"id": str(m.id), "role": m.role, "content": m.content, "created_at": m.created_at}
        for m in messages
    ]

async def update_source_count(conversation_id: str, count: int):
    
    conv = await Conversation.find_one(Conversation.conversation_id == conversation_id)
    if conv:
        conv.source_count = count
        conv.last_activity = datetime.now(timezone.utc)
        await conv.save()

async def get_last_message(conversation_id: str, role: str) -> Message:
    return await Message.find(
        Message.conversation_id == conversation_id,
        Message.role == role
    ).sort("-created_at").first_or_none()

async def delete_pinecone_db(conversation_id: str, vector_ids: list[str]):
    await delete_vectorize(conversation_id, vector_ids)

async def delete_source_db(conversation_id: str, source_id: PydanticObjectId):
    source_doc = await Source.find_one(Source.id == source_id)

    if not source_doc:
        return {"status": "error", "message": "Source not found"}

    if source_doc.conversation_id != conversation_id:
        return {"status": "error", "message": "Source does not belong to this conversation"}

    deleted_url = source_doc.url 

    await source_doc.delete()

    await delete_pinecone_db(conversation_id, source_doc.vector_ids)

    count = await Source.find(Source.conversation_id == conversation_id).count()
    await update_source_count(conversation_id, count)

    return {
        "status": "success",
        "message": "Source deleted successfully",
        "deleted": {
            "id": source_id,
            "url": deleted_url
        }
    }

async def add_scrapedURL(conversation_id: str, query: str, url_list: list[dict]):
    await ScrapedURLs(conversation_id=conversation_id, query=query, url_list=url_list).insert()

async def delete_scraped_urls(conversation_id: str, query: str):
    await ScrapedURLs.find(ScrapedURLs.conversation_id == conversation_id, ScrapedURLs.query == query).delete()