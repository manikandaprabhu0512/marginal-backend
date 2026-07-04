from tools.vectorize_tool import vectorize_page


async def process_page(page: dict, conversation_id: str) -> dict:
    
    result = {"storage": None, "title": None, "url": None, "vector_ids": None}
    
    try:
        vector_ids = await vectorize_page(conversation_id, page["url"], page["title"], page["raw_content"])

        if vector_ids:

            result["storage"] = {"status": "stored"}
            result["title"] = page["title"]
            result["url"] = page["url"]
            result["vector_ids"] = vector_ids

    except Exception as e:
        result["storage"] = {"status": "failed", "reason": str(e)}
    
    return result