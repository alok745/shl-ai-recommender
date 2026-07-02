from typing import List


def build_recommendations(results: List[dict]):

    recommendations = []

    for item in results[:10]:

        recommendations.append(
            {
                "name": item["name"],
                "url": item["link"],
                "reason": (
                    f"Suitable for {', '.join(item.get('keys', [])[:3])}"
                    if item.get("keys")
                    else "Relevant assessment"
                ),
            }
        )

    return recommendations