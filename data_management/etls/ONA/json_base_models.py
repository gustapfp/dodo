from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    core: bool
    description: str
    evidence: str
    id: str
    orientation: str
    level: int


class Subsection(BaseModel):
    id: str
    level1: List[Question]
    level2: List[Question]
    title: str


class Section(BaseModel):
    id: str
    title: str
    subsections: List[Subsection]
    level3: List[Question]
