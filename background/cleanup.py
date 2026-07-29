import logging

from db.crud import delete_scraped_urls

logger = logging.getLogger(__name__)


async def cleanup_ingestion(conversation_id: str,query: str) -> None:
    """Remove temporary ingestion data after the ingestion pipeline completes."""

    print("Cleaning up ingestion...")
    try:
        logger.info("Cleaning temporary ingestion data | Conversation=%s",conversation_id)

        print("Deleting temporary ingestion data...")
        await delete_scraped_urls(conversation_id,query)
        print("Deleted temporary ingestion data...")

        logger.info("Cleanup completed | Conversation=%s",conversation_id)

    except Exception:
        logger.exception("Cleanup failed | Conversation=%s",conversation_id)