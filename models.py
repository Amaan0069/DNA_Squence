# models.py
from pydantic import BaseModel
from typing import Optional

class CompareRequest(BaseModel):
    id1: str
    id2: str

class AskRequest(BaseModel):
    question: str
