import json

from agents.confidence_agent import get_confidence_agent
from agents.larger_model_agent import get_larger_model_agent
from agents.query_understanding_agent import get_query_understanding_agent
from agents.smaller_model_agent import get_smaller_model_agent
from db.crud import get_history, get_last_message, save_message
from helper.json_parser import parse_agent_json
from helper.serializer import _message_to_dict
from helper.sse_event import sse_event
from tools.retriever_tool import retrieve_context

CONFIDENCE_THRESHOLD = 0.75


async def run_chat(conversation_id, message, excluded_urls=None, skip_save_user: bool = False):
    yield sse_event("fetching_history", {})
    history = await get_history(conversation_id)
    
    if not skip_save_user:
        user_message = await save_message(conversation_id, "user", message)
    else:
        user_message = await get_last_message(conversation_id, role="user")

    yield sse_event("understanding_query", {})
    understanding_agent = get_query_understanding_agent()
    query_payload = json.dumps({"query": message, "history": history})
    result = await understanding_agent.ainvoke({"messages": [{"role": "user", "content": query_payload}]})
    data = parse_agent_json(result["messages"][-1].content)
    print("Understanding Agent Result: ", data)
    query_type = data["type"]
    rewritten_query = data["rewritten_query"]
    direct_answer = data["direct_answer"]

    if query_type in ("filler", "off_topic"):
        if query_type == "off_topic":
            direct_answer = f"{direct_answer}\n\n*Note: This isn't from your gathered sources — based on general knowledge.*"
        assistant_message = await save_message(conversation_id, "assistant", direct_answer)
        yield sse_event("answer_ready", _response(
            conversation_id, user_message, assistant_message,
            confidence=None, model_used=None,
            source="knowledge_base" if query_type == "filler" else "general_knowledge"
        ))
        yield sse_event("done", {})
        return

    yield sse_event("retrieving_context", {})
    context = await retrieve_context(conversation_id, rewritten_query, excluded_urls)

    yield sse_event("smaller_model_generating_answer", {})
    input_payload = json.dumps({"query": rewritten_query, "context": context, "history": history, "excluded_urls": excluded_urls})
    smaller_agent = await get_smaller_model_agent(conversation_id)
    result = await smaller_agent.ainvoke({"messages": [{"role": "user", "content": input_payload}]})
    data = parse_agent_json(result["messages"][-1].content)
    answer, source = data["answer"], data["source"]

    if source == "general_knowledge":
        answer = f"{answer}\n\n*Note: This isn't from your gathered sources — based on general knowledge.*"
        assistant_message  = await save_message(conversation_id, "assistant", answer)
        result = _response(conversation_id, user_message, assistant_message , confidence=None, model_used="smaller_model", source=source)
        yield sse_event("answer_ready", result)
        yield sse_event("done", {})
        return
    
    confidence_agent = get_confidence_agent()
    conf_payload = json.dumps({"query": rewritten_query, "context": context, "answer": answer, "source": source})
    yield sse_event("checking_confidence", {})
    conf_result = await confidence_agent.ainvoke({"messages": [{"role": "user", "content": conf_payload}]})
    confidence = parse_agent_json(conf_result["messages"][-1].content)["confidence"]

    if confidence >= CONFIDENCE_THRESHOLD:
        assistant_message  = await save_message(conversation_id, "assistant", answer)
        result = _response(conversation_id, user_message, assistant_message , confidence, "smaller_model", source)
        yield sse_event("answer_ready", result)
        yield sse_event("done", {})
        return

    yield sse_event("larger_model_generating_answer", {})
    larger_agent = await get_larger_model_agent(conversation_id)
    larger_result = await larger_agent.ainvoke({"messages": [{"role": "user", "content": input_payload}]})
    larger_data = parse_agent_json(larger_result["messages"][-1].content)
    answer = larger_data["answer"]
    source = larger_data["source"]

    #No need to check for confidence here. Be knowledge_base or general_knowledge we're returning anyways

    if source == "general_knowledge":
        answer = f"{answer}\n\n*Note: This isn't from your gathered sources — based on general knowledge.*"

    assistant_message  = await save_message(conversation_id, "assistant", answer)
    result = _response(conversation_id, user_message, assistant_message , None, "larger_model", source)
    yield sse_event("answer_ready", result)
    yield sse_event("done", {})

def _response(conversation_id, user, assistant, confidence, model_used, source):
    return {
        "conversation_id": conversation_id,
        "user": _message_to_dict(user),
        "assistant": _message_to_dict(assistant),
        "confidence": confidence,
        "model_used": model_used,
        "source": source,
    }