def is_compare_query(query):

    query = query.lower()

    return any(
        word in query
        for word in [
            "compare",
            "comparison",
            "difference",
            "vs",
            "versus",
        ]
    )