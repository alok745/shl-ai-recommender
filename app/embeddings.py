import json
import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

CATALOG_PATH = "app/catalog.json"
INDEX_PATH = "vector_store/shl.index"
METADATA_PATH = "vector_store/metadata.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_text(item):
    return f"""
Name: {item.get('name', '')}
Description: {item.get('description', '')}
Skills: {', '.join(item.get('keys', []))}
Job Levels: {', '.join(item.get('job_levels', []))}
Languages: {', '.join(item.get('languages', []))}
Duration: {item.get('duration', '')}
Remote: {item.get('remote', '')}
Adaptive: {item.get('adaptive', '')}
"""


def create_embeddings():
    os.makedirs("vector_store", exist_ok=True)

    catalog = load_catalog()

    texts = [build_text(item) for item in catalog]

    print(f"Creating embeddings for {len(texts)} assessments...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings.astype("float32"))

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(catalog, f)

    print("✅ FAISS index created successfully!")
    print(f"Assessments indexed: {len(catalog)}")


if __name__ == "__main__":
    create_embeddings()