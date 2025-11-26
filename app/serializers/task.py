from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class TaskOutputMini(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    content: Optional[str] = None


class TaskCreate(BaseModel):
    title: str
    content: Optional[str] = None
    author_id: str
    recipient_id: str


class TaskOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    title: str
    content: Optional[str] = None
    author_id: str
    recipient_id: str

    # NO IMPORT !!! → utiliser les noms en string
    author: "EmployeeOutputMini"    # type: ignore
    recipient: "EmployeeOutputMini" # type: ignore
