import json


def sse_event(type: str, data: dict) -> str:
    return f"event: {type}\ndata: {json.dumps(data)}\n\n"