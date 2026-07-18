import re

import httpx
from bs4 import BeautifulSoup
from fastapi import UploadFile

from helper.load_page import load_page
from helper.text_extractors import (EXTRACTORS, _extract_pdf, _get_ext,
                                    _title_from_filename)
from tools.vectorize_tool import vectorize_page


async def _process_file(conversation_id: str, file: UploadFile) -> dict:
    filename = file.filename
    ext = _get_ext(filename)

    if ext not in EXTRACTORS:
        return {"status": "failed", "reason": f"Unsupported file type: .{ext}"}

    file_bytes = await file.read()

    try:
        text = EXTRACTORS[ext](file_bytes)
    except Exception as e:
        return {"status": "failed", "reason": f"Text extraction failed: {str(e)}"}

    title = _title_from_filename(filename)
    url = f"file://{filename}"
    source_type = "pdf"

    vectorIds = await vectorize_page(conversation_id, url, title, text)
    return {"status": "stored", "title": title, "url": url, "source_type": source_type, "vector_ids": vectorIds}


async def _process_url(conversation_id: str, url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        content_type = response.headers.get("content-type", "")

        if "pdf" in content_type or url.lower().endswith(".pdf"):
            text = _extract_pdf(response.content)
            title = url.split("/")[-1].replace(".pdf", "").replace("-", " ").title()
            source_type = "pdf"
        else:
            page = {"url": url}
            result = await load_page(page)   
            title = result["title"]
            text = result["raw_content"]
            source_type = "url"

    except Exception as e:
        return {"status": "failed", "reason": f"Failed to load URL: {str(e)}"}

    await vectorize_page(conversation_id, url, title, text)
    return {"status": "stored", "title": title, "url": url, "source_type": source_type}