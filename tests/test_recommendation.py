from app.retriever import search_catalog
from app.recommendation import build_recommendations

results = search_catalog("Java Developer")

recommendations = build_recommendations(results)

for r in recommendations:
    print(r)