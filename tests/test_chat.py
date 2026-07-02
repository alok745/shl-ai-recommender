from app.chatbot import chat

messages = [
    {
        "role":"user",
        "content":"I need a Java developer assessment"
    }
]

response = chat(messages)

print(response)