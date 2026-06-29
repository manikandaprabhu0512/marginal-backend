from langgraph.types import Command

from graph.chat_graph.chat_graph import chat_graph


async def resume_chat_graph(
    conversation_id: str,
    decision: str,
):
    config = {
        "configurable": {
            "thread_id": conversation_id,
        }
    }

    async for event in chat_graph.astream(
        Command(resume=decision),
        config=config,
    ):
        print("=" * 100)
        print(event)

    return