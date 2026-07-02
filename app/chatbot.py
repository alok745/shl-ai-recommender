from app.guardrails import is_allowed
from app.utils import is_compare_query
from app.retriever import search_catalog
from app.recommendation import build_recommendations
from app.llm import generate
from app.memory import build_search_query
from app.clarification import needs_clarification as should_clarify
from app.memory import (
    get_latest_user_message,
    conversation_text,
)


def build_context(results):

    context = ""

    for item in results:

        context += f"""
Assessment: {item['name']}
Description: {item.get('description', '')}
Skills: {", ".join(item.get("keys", []))}
Job Levels: {", ".join(item.get("job_levels", []))}
Duration: {item.get("duration", "")}
Remote: {item.get("remote", "")}
Adaptive: {item.get("adaptive", "")}
URL: {item["link"]}

"""

    return context


def chat(messages):

    latest_message = get_latest_user_message(messages)

    # -----------------------
    # Get previous user message
    # -----------------------

    previous_user = ""

    user_messages = []

    for msg in messages:

        if isinstance(msg, dict):

            if msg.get("role") == "user":
                user_messages.append(msg.get("content", ""))

        else:

            if getattr(msg, "role", "") == "user":
                user_messages.append(getattr(msg, "content", ""))

    if len(user_messages) >= 2:
        previous_user = user_messages[-2]

    # -----------------------
    # Guardrails
    # -----------------------

    if not is_allowed(latest_message):

        return {
            "response": "I can only answer questions related to SHL assessments.",
            "recommendations": [],
            "needs_clarification": False,
        }

    # -----------------------
    # Compare Mode
    # -----------------------

    compare_mode = is_compare_query(latest_message)

    if compare_mode:

        retrieved = search_catalog(latest_message)
        requested = latest_message.lower()
        filtered = []
        for item in retrieved:
            if item["name"].lower() in requested:
                filtered.append(item)
                if filtered:
                    retrieved = filtered
            
        

        recommendations = build_recommendations(retrieved)

        context = build_context(retrieved)

        prompt = f"""
You are an SHL Assessment Recommendation Assistant.

The user wants to compare the requested assessments.

Compare ONLY the assessments present in the Context.

For each assessment include:
- Purpose
- Skills measured
- Job levels
- Duration
- Adaptive
- Remote testing

Finish with a short recommendation.

Do not mention any other assessments.
Do not invent information.


Context:

{context}
"""

        answer = generate(prompt)

        return {
            "response": answer,
            "recommendations": recommendations,
            "needs_clarification": False,
        }

    # -----------------------
    # Clarification
    # -----------------------

    if should_clarify(latest_message):

        return {
            "response": "What experience level is this Java developer position? (Entry, Mid or Senior)",
            "recommendations": [],
            "needs_clarification": True,
        }

    # -----------------------
    # Build search query
    # -----------------------

    search_query = latest_message
    if len(search_query.split()) < 2:
        return {
            "response": "Please provide more details about the role or assessment you are looking for.",
            "recommendations": [],
            "needs_clarification": True,
            }
            

    if latest_message.lower() in [
        "entry",
        "junior",
        "mid",
        "senior",
        "lead",
        "experienced",
    ]:

        search_query = previous_user + " " + latest_message

    # -----------------------
    # Retrieval
    # -----------------------

    retrieved = search_catalog(search_query)
    
    if not retrieved:
        return {
            "response": "Sorry, I couldn't find any matching SHL assessments.",
            "recommendations": [],
            "needs_clarification": False,
            }
            

    recommendations = build_recommendations(retrieved)

    context = build_context(retrieved)

    # -----------------------
    # Prompt
    # -----------------------

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.
The user wants to compare SHL assessments.

STRICT RULES

1. Compare ONLY assessments found in Context.
2. Never invent information.
3. Show the comparison in bullet points.

For each assessment include:

- Assessment Name
- Skills Measured
- Job Levels
- Duration
- Adaptive
- Remote Testing

Finish with:

Recommendation:
Explain when each assessment should be chosen.

Context:

{context}

Conversation:

{conversation_text(messages)}
"""

    answer = generate(prompt)

    clarification_required = any(
        word in answer.lower()
        for word in [
            "which",
            "what",
            "please specify",
            "clarify",
            "could you",
            "tell me more",
        ]
    )

    return {
        "response": answer,
        "recommendations": recommendations,
        "needs_clarification": clarification_required,
    }