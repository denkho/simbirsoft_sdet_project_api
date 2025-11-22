from pydantic import BaseModel
from typing import List, Optional


class Addition(BaseModel):
    additional_info: str
    additional_number: int
    id: Optional[int] = None


class Entity(BaseModel):
    id: Optional[int] = None
    title: str
    verified: bool
    important_numbers: List[int]
    addition: Addition
