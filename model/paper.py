from pydantic import BaseModel
from typing import List, Optional
from backend.models.section import PaperSection


class ResearchPaper(BaseModel):
    paper_id: str
    title: str
    authors: List[str]
    abstract: str
    sections: List[PaperSection]
    full_text: str              # ✅ ADD THIS
    year: Optional[int] = None
    venue: Optional[str] = None
    keywords: List[str] = []
    references: List[str] = []
