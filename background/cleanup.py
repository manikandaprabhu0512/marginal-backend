import logging

from db.crud import delete_scraped_urls

logger = logging.getLogger(__name__)


async def cleanup_ingestion(conversation_id: str,query: str) -> None:
    """Remove temporary ingestion data after the ingestion pipeline completes."""

    try:
        logger.info("Cleaning temporary ingestion data | Conversation=%s",conversation_id)

        await delete_scraped_urls(conversation_id,query)

        logger.info("Cleanup completed | Conversation=%s",conversation_id)

    except Exception:
        logger.exception("Cleanup failed | Conversation=%s",conversation_id)