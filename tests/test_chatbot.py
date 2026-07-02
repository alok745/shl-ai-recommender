from app.chatbot import chat

response = chat("I need a Java developer assessment")

print(response["answer"])

print("\nRecommended Assessments:\n")

for item in response["recommendations"]:
    print("-", item["name"])