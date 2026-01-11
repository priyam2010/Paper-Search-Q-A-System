import re
from typing import List
from backend.models.section import PaperSection

SECTION_HEADERS = [
    "abstract",
    "introduction",
    "related_work",
    "methodology",
    "methods",
    "experiments",
    "result",
    "discussion",
    "conclusion",
    "refrences"    
]
def extract_sections(text:str) -> list[PaperSection]:
    sections = []
    lower_text = text.lower()
    indices = []
    for header in SECTION_HEADERS:
        match = re.search(rf"\n{header}\n",lower_text)
        if match:
            indices.append((header,match.start()))
    indices.sort(key = lambda x: x[1])
    for i in range(len(indices)):
        section_name = indices[i][0]
        start = indices[i][1]
        end = indices[i+1][1] if i+1 < len(indices) else len(text)
        
        content = text[start:end].strip()
        sections.append(PaperSection(section_name = section_name,content = content))
    return sections
