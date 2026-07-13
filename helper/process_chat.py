import asyncio
import json
import re
import time

from fastapi import UploadFile

from agents.intent_classifier_agent import get_intent_classifier_agent
from db.crud import get_or_create_conversation, save_message, save_sources
from flows.add_source_flow import URL_PATTERN, run_add_source
from graph.chat_graph.chat_event_stream import chat_event_stream
from helper.json_parser import parse_agent_json
from helper.serializer import _message_to_dict
from helper.sse_event import sse_event
from telemetry.metrics import chat_duration, chat_requests


async def process_chat(conversation_id: str, message: str, files: list[UploadFile], excluded_urls: str):

    start = time.perf_counter()
    
    try:
        if len(message.strip()) > 200:
            yield sse_event("error", {"message": "Message too long. Paste URLs or attach files to add sources."})
            return

        if not await get_or_create_conversation(conversation_id):
            yield sse_event("error", {"message": "Conversation not found"})
            return
        
        chat_requests.add(1)

        excluded = json.loads(excluded_urls)
        yield sse_event("checking_for_files", {})
        has_files = files and any(f.filename for f in files)

        if has_files:
            user_message = await save_message(conversation_id, "user", message)
            yield sse_event("uploading_files", {"count": len([f for f in files if f.filename])})
            results = await asyncio.gather(
                *[run_add_source(conversation_id, file=f) for f in files if f.filename],
                return_exceptions=True
            )
            stored = []
            failed = []

            for r in results:
                if isinstance(r, Exception):
                    failed.append({"status": "failed", "reason": str(r)})
                elif isinstance(r, dict) and r.get("status") == "failed":
                    failed.append(r)
                else:
                    stored.append(r)

            yield sse_event("file_stored", {"count": len(stored)})

            if failed and not stored:
                yield sse_event("error", {"type": "source_failed", "sources": failed})
                return

            if failed and stored:
                yield sse_event("partial_success", {"stored": stored, "failed": failed, "count": len(stored)})
            
            sources = [
                {"title": r["title"], "url": r["url"], "source_type": r["source_type"]}
                for r in stored
            ]
            await save_sources(conversation_id, sources)

            titles = ", ".join(r["title"] for r in stored)
            yield sse_event("sources_saved", {"sources": sources})

            if not message.strip():
                assistant_message = await save_message(conversation_id, "assistant", f"Got it! I've added {titles} to your knowledge base.")
                yield sse_event("answer_ready", {
                    "user": _message_to_dict(user_message),
                    "assistant": _message_to_dict(assistant_message),
                    "model_used": None,
                    "source": None
                })
                yield sse_event("done", {})
                return
            
            classifier = get_intent_classifier_agent()
            clf_result = await classifier.ainvoke({
                "messages": [{"role": "user", "content": json.dumps({"message": message})}]
            })
            intent = parse_agent_json(clf_result["messages"][-1].content)["type"]

            if intent == "source_only":
                assistant_message = await save_message(conversation_id, "assistant", f"Got it! I've added {titles} to your knowledge base.")
                yield sse_event("answer_ready", {
                    "user": _message_to_dict(user_message),
                    "assistant": _message_to_dict(assistant_message),
                    "model_used": None,
                    "source": None
                })
                yield sse_event("done", {})
                return

            enriched_message = f"{message} [Context: user just added these sources: {titles}]"
            async for item in chat_event_stream(
                conversation_id=conversation_id,
                message=enriched_message,
                excluded_urls=excluded,
                skip_save_user=False,
            ):
                yield item

            return

        has_url = bool(message and URL_PATTERN.match(message.strip()))

        if has_url:
            yield sse_event("loading_url", {})
            url = re.search(r'https?://\S+', message).group()
            result = await run_add_source(conversation_id, content=url)
            if result.get("status") == "failed":
                yield sse_event("error", {"type": "source_failed", "source": result})
                return
            yield sse_event("source_saved", result)
            yield sse_event("done", {})
            return

        async for item in chat_event_stream(
            conversation_id=conversation_id,
            message=message,
            excluded_urls=excluded,
            skip_save_user=False,
        ):
            yield item
    
    finally:
        chat_duration.record(
            time.perf_counter() - start
        )