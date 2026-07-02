LEVEL_WORDS = [
    "entry",
    "junior",
    "mid",
    "senior",
    "lead",
    "experienced",
]

ROLE_WORDS = [
    "java",
    "python",
    "frontend",
    "backend",
    "developer",
    "engineer",
]

COMPARE_WORDS = [
    "compare",
    "difference",
    "vs",
    "versus",
]


def needs_clarification(query):

    q = query.lower()

    # Never ask clarification for comparison
    if any(word in q for word in COMPARE_WORDS):
        return False

    if any(word in q for word in ROLE_WORDS):

        if not any(level in q for level in LEVEL_WORDS):
            return True

    return False