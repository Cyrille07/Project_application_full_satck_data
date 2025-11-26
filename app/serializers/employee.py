from pydantic import BaseModel, ConfigDict
from typing import List


class EmployeeOutputMini(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    role: str


class EmployeeCreate(BaseModel):
    name: str
    password: str
    role: str


class EmployeeOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    role: str

    # NO IMPORT !!! → utiliser des strings
    tasks_written: List["TaskOutputMini"] = []  # type: ignore
    tasks_received: List["TaskOutputMini"] = []  # type: ignore
