import json
import re


def parse_agent_json(raw_content: str) -> dict:
    cleaned = raw_content.strip()
    if not cleaned:
        raise ValueError("Agent returned empty content")
    cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned)
    cleaned = re.sub(r'\n?```$', '', cleaned)
    cleaned = cleaned.strip()
    try:
        parsed = json.loads(cleaned, strict=False)
        if "answer" in parsed:
            parsed["answer"] = parsed["answer"].replace("\\n", "\n")
        return parsed
    except json.JSONDecodeError as e:
        raise ValueError(f"Agent returned invalid JSON: {e}\nRaw: {raw_content[:500]}")