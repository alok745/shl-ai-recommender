import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "vector_store/shl.index"
METADATA_PATH = "vector_store/metadata.pkl"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load catalog
with open(METADATA_PATH, "rb") as f:
    catalog = pickle.load(f)

# --------------------------------------------------
# Query Expansion
# --------------------------------------------------

ROLE_HINTS = {
    "java": "core java java developer java 8 j2ee spring spring boot java framework java ee object oriented programming",
    "python": "python django flask backend api programming",
    "frontend": "javascript react angular html css frontend ui web",
    "backend": "node express api backend microservices rest",
    "sales": "sales negotiation customer relationship account executive",
    "finance": "finance accounting banking audit financial analyst",
    "manager": "leadership management supervisor team lead people management",
}

JAVA_PRIORITY = [
    "Core Java (Entry Level) (New)",
    "Core Java (Advanced Level) (New)",
    "Java 8 (New)",
    "Java Frameworks (New)",
    "Java Web Services (New)",
]

LEVEL_PRIORITY = {
    "entry": [
        "Core Java (Entry Level) (New)",
        "Java Fundamentals (New)",
        "Java 8 (New)"
    ],

    "mid": [
        "Core Java (Advanced Level) (New)",
        "Java Frameworks (New)",
        "Java 8 (New)",
        "Java Web Services (New)"
    ],

    "senior": [
        "Core Java (Advanced Level) (New)",
        "Java Frameworks (New)",
        "Java Web Services (New)",
        "Enterprise Java Beans (New)",
        "Java Platform Enterprise Edition 7 (Java EE 7)"
    ]
}


def expand_query(query: str) -> str:
    query_lower = query.lower()

    for keyword, expansion in ROLE_HINTS.items():
        if keyword in query_lower:
            return query + " " + expansion

    return query


# --------------------------------------------------
# Catalog Filter
# --------------------------------------------------

def filter_catalog(query: str):

    q = query.lower()

    filtered = []

    for item in catalog:

        text = (
            item.get("name", "")
            + " "
            + item.get("description", "")
            + " "
            + " ".join(item.get("keys", []))
        ).lower()

        if "java" in q:

            java_keywords = [
                "java",
                "core java",
                "java ee",
                "j2ee",
                "spring",
                "spring boot",
            ]

            if any(keyword in text for keyword in java_keywords):
                filtered.append(item)

        elif "python" in q:

            if "python" in text:
                filtered.append(item)

        elif "frontend" in q:

            if any(
                word in text
                for word in [
                    "javascript",
                    "react",
                    "angular",
                    "frontend",
                    "html",
                    "css",
                ]
            ):
                filtered.append(item)

        elif "backend" in q:

            if any(
                word in text
                for word in [
                    "backend",
                    "node",
                    "express",
                    "api",
                ]
            ):
                filtered.append(item)

        elif "sales" in q:

            if "sales" in text:
                filtered.append(item)

        elif "finance" in q:

            if "finance" in text or "account" in text:
                filtered.append(item)

        else:
            filtered.append(item)

    return filtered


# --------------------------------------------------
# Keyword Re-ranking
# --------------------------------------------------

def rerank(query: str, results):

    query_words = query.lower().split()

    ranked = []

    for item in results:

        score = 0

        name = item.get("name", "").lower()
        description = item.get("description", "").lower()
        keys = " ".join(item.get("keys", [])).lower()

        text = f"{name} {description} {keys}"

        for word in query_words:

            if word in name:
                score += 50

            if word in keys:
                score += 35

            if word in description:
                score += 20

            if word in text:
                score += 5

        ranked.append((score, item))

    ranked.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in ranked]


# --------------------------------------------------
# Main Search
# --------------------------------------------------

def search_catalog(query: str, top_k: int = 10):

    expanded_query = expand_query(query)

    filtered_catalog = filter_catalog(expanded_query)

    if not filtered_catalog:
        filtered_catalog = catalog

    texts = [
        item.get("name", "") + " " + item.get("description", "")
        for item in filtered_catalog
    ]

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    temp_index = faiss.IndexFlatL2(embeddings.shape[1])

    temp_index.add(embeddings)

    query_embedding = model.encode([expanded_query])

    query_embedding = np.array(query_embedding).astype("float32")

    k = min(50, len(filtered_catalog))

    distances, indices = temp_index.search(query_embedding, k)

    candidates = []

    for idx in indices[0]:
        if idx != -1:
            candidates.append(filtered_catalog[idx])

        ranked = rerank(query, candidates)

    # ------------------------------------------
    # Prioritize Java Assessments
    # ------------------------------------------

    q = query.lower()
    priority = []

    if "java" in q:

        if "entry" in q or "junior" in q:
            priority = LEVEL_PRIORITY["entry"]

        elif "mid" in q:
            priority = LEVEL_PRIORITY["mid"]

        elif (
            "senior" in q
            or "lead" in q
            or "experienced" in q
        ):
            priority = LEVEL_PRIORITY["senior"]

        else:
            priority = JAVA_PRIORITY

    if priority:

        ordered = []

        for assessment_name in priority:

            for item in ranked:

                if item.get("name") == assessment_name:
                    ordered.append(item)

        for item in ranked:

            if item not in ordered:
                ordered.append(item)

        ranked = ordered

    return ranked[:top_k]