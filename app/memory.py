def get_latest_user_message(messages):
    """
    Returns latest user message.
    """

    for message in reversed(messages):

        if isinstance(message, dict):

            if message.get("role") == "user":
                return message.get("content", "")

        else:

            if getattr(message, "role", "") == "user":
                return getattr(message, "content", "")

    return ""


def conversation_text(messages):
    """
    Convert conversation into readable text.
    """

    lines = []

    for message in messages:

        if isinstance(message, dict):

            role = message.get("role", "")
            content = message.get("content", "")

        else:

            role = getattr(message, "role", "")
            content = getattr(message, "content", "")

        lines.append(f"{role.capitalize()}: {content}")

    return "\n".join(lines)


def previous_user_messages(messages):
    """
    Returns all previous user messages except the latest.
    """

    history = []

    for message in messages:

        if isinstance(message, dict):

            if message.get("role") == "user":
                history.append(message.get("content", ""))

        else:

            if getattr(message, "role", "") == "user":
                history.append(getattr(message, "content", ""))

    return history[:-1]


def build_search_query(messages):
    """
    Build complete search query from conversation.
    """

    history = previous_user_messages(messages)

    latest = get_latest_user_message(messages)

    if history:
        return " ".join(history + [latest])

    return latest