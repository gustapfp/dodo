from pydantic import BaseModel
from typing import List

class Question(BaseModel):
  id: str
  description: str
  guidance: str
  evidence: str

class Subsection(BaseModel):
  subsectionId: str
  subsectionTitle:str
  level1: List[Question]
  level2: List[Question]

class Section(BaseModel):
  sectionId: str
  sectionTitle: str
  subsections: List[Subsection]
  level3: List[Question]