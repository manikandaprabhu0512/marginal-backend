from graph.chat_graph.chat_graph import chat_graph


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

    async for _ in chat_graph.astream(
        {
            "conversation_id": conversation_id,
            "message": message,
            "excluded_urls": excluded_urls,
            "skip_save_user": skip_save_user,
            "confidence": None,
        },
        config=config,
    ):
        pass