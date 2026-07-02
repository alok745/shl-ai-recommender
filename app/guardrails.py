OUT_OF_SCOPE = [
    "ipl",
    "cricket",
    "football",
    "movie",
    "politics",
    "president",
    "prime minister",
    "bitcoin",
    "weather",
    "recipe",
    "hack",
    "password",
    "ignore previous",
    "system prompt",
]


def is_allowed(question: str):

    q = question.lower()

    for word in OUT_OF_SCOPE:
        if word in q:
            return False

    return True