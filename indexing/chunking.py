from typing import List, Dict
from backend.models.paper import ResearchPaper

MAX_CHUNK_SIZE = 800


from typing import List


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Simple character-based chunking.
    Guaranteed to return chunks if text is non-empty.
    """

    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

    return chunks



def chunk_paper(paper: ResearchPaper) -> List[Dict]:
    all_chunks = []

    # ✅ 1. Try section-based chunking
    for section in paper.sections:
        section_chunks = chunk_text(section.content)

        for chunk in section_chunks:
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "paper_id": paper.paper_id,
                    "title": paper.title,
                    "section": section.section_name,
                    "year": paper.year
                }
            })

    # ✅ 2. FALLBACK: no sections found → use full text
    if not all_chunks:
        print("⚠️ No section chunks found — falling back to full-text chunking")

        fallback_chunks = chunk_text(paper.full_text)

        for chunk in fallback_chunks:
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "paper_id": paper.paper_id,
                    "title": paper.title,
                    "section": "full_text",
                    "year": paper.year
                }
            })

        
           