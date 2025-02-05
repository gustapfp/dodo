from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    id: str
    description: str
    guidance: str
    evidence: str
    # core: bool
    # orientation: str


class Subsection(BaseModel):
    # id: str
    subsectionId: str
    subsectionTitle: str
    # title: str
    level1: List[Question]
    level2: List[Question]


class Section(BaseModel):
    # id: str
    sectionId: str
    sectionTitle: str
    subsections: List[Subsection]
    level3: List[Question]
