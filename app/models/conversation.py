from app.core.db_connect import Base
from sqlalchemy import Column, UUID, Integer, String, DateTime
from typing import List

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(UUID, index=True)
    role = Column(String)
    content = Column(String)
    create_time = Column(DateTime)

class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(UUID, primary_key=True, index=True)
    user_id = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    messages = Column(List[Message])