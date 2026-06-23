import re

from fastapi import UploadFile
from helper.source_handlers import _process_file, _process_url

URL_PATTERN = re.compile(r'^https?://', re.IGNORECASE)

async def run_add_source(
    conversation_id: str,
    content: str = "",
    file: UploadFile = None,
) -> dict:

    if file and file.filename:
        return await _process_file(conversation_id, file)

    if content and URL_PATTERN.match(content.strip()):
        return await _process_url(conversation_id, content.strip())

    return {"status": "failed", "reason": "No valid input provided"}