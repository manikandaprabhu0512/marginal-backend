import logging

from helper.checkpointer import checkpointer

logger = logging.getLogger(__name__)


async def cleanup_checkpoints(conversation_id: str):
    try:
        await checkpointer.adelete_thread(conversation_id)
    except Exception:
        logger.exception(
            "Failed to cleanup checkpoints for %s",
            conversation_id,
        )