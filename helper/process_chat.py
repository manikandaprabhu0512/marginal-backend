import asyncio
import json
import re
import time

from cloudinary.exceptions import Error
from cloudinary.uploader import upload
from fastapi import UploadFile

import config.cloudinary_config
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
    message = message or ""

    print("Message: ", message)
    print("Files: ", files)
    if (not message or not message.strip()) and not files:
        yield sse_event("error", {"message": "No message or file both are not found. Please enter one to move forward"});
        yield sse_event("done", {})
        return

    
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

        print("Files found:", has_files)

        if has_files:
            valid_files = [f for f in files if f.filename]
            yield sse_event("uploading_files", {"count": len(valid_files)})

            uploaded_results = []
            files_to_process = []

            try:
                for file in valid_files:
                    try:
                        await file.seek(0)
                        print("Uploading Files>>>>")
                        result = upload(file.file, resource_type="auto", access_mode="public")
                        print("File Uploaded....")

                        file_url = result.get("secure_url") or result.get("url")
                        if not file_url:
                            raise ValueError("Cloudinary upload did not return a URL")

                        uploaded_results.append({
                            "filename": file.filename,
                            "url": file_url,
                            "public_id": result.get("public_id"),
                            "status": "success"
                        })
                        files_to_process.append(file)
                        await file.seek(0)
                    except Error as e:
                        uploaded_results.append({
                            "filename": file.filename,
                            "status": "failed",
                            "error": str(e)
                        })
                    except Exception as e:
                        uploaded_results.append({
                            "filename": file.filename,
                            "status": "failed",
                            "error": str(e)
                        })
                    finally:
                        print("Cloudinary upload result: ", uploaded_results)

                failed_uploads = [r for r in uploaded_results if r["status"] == "failed"]
                successful_uploads = [r for r in uploaded_results if r["status"] == "success"]

                if failed_uploads and not successful_uploads:
                    yield sse_event("error", {"type": "upload_failed", "files": failed_uploads})
                    return

                if failed_uploads:
                    yield sse_event("partial_upload", {
                        "uploaded": successful_uploads,
                        "failed": failed_uploads,
                        "count": len(successful_uploads),
                    })

                user_message = await save_message(
                    conversation_id,
                    "user",
                    message,
                    file_url=successful_uploads[0]["url"] if successful_uploads else None,
                )

                results = await asyncio.gather(
                    *[run_add_source(conversation_id, file=f) for f in files_to_process],
                    return_exceptions=True
                )
            finally:
                for file in valid_files:
                    file.file.close()

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
                {"title": r["title"], "url": r["url"], "source_type": r["source_type"], "vector_ids":r["vector_ids"]}
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
                skip_save_user=True,
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
