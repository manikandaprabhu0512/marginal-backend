def _message_to_dict(message) -> dict:
    return {
        "id": str(message.id),
        "conversation_id": message.conversation_id,
        "role": message.role,
        "content": message.content,
        "file_url": message.file_url,
        "created_at": message.created_at.isoformat() if message.created_at else None,
    }
