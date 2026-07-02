from app.chatbot import chat

messages = [
    {
        "role": "user",
        "content": "Who won IPL 2025?"
    }
]

print(chat(messages))