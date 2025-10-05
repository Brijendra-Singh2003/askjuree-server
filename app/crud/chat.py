# from typing import Optional
from pydantic import BaseModel

class ChatMessageCreate(BaseModel):
    role: str
    content: str

class ChatMessage(ChatMessageCreate):
    id: int

chat = [
    ChatMessage(
        id=0,
        role="system",
        content="You are a kind person names jury, you help freshers avoide any exploitation that can happen in their company.",
    ),
]

def add_chat_message(message: ChatMessageCreate):
    new_message = ChatMessage(role=message.role, content=message.content, id=len(chat))
    chat.append(new_message)

def get_chat_message():
    return chat
