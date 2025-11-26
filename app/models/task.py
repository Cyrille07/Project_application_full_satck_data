from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import BaseSQL
import uuid

class Task(BaseSQL):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    author_id = Column(String, ForeignKey("employees.id"))
    recipient_id = Column(String, ForeignKey("employees.id"))

    # RELATIONS
    author = relationship("Employee", back_populates="tasks_written", foreign_keys=[author_id])
    recipient = relationship("Employee", back_populates="tasks_received", foreign_keys=[recipient_id])
