from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import BaseSQL
import uuid


class Employee(BaseSQL):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False, unique = True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # relations
    tasks_written = relationship("Task",back_populates="author",foreign_keys="Task.author_id")

    tasks_received = relationship("Task", back_populates="recipient",foreign_keys="Task.recipient_id")
