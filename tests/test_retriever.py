from app.retriever import search_catalog

query = "Java developer assessment"

results = search_catalog(query)

print("=" * 50)

for i, item in enumerate(results, start=1):
    print(f"{i}. {item['name']}")
    print(item["link"])
    print()