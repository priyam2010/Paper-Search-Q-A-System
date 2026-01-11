from backend.rag.retriever import Retriever
from backend.llm.groq_client import GroqLLM

def build_prompt(question, contexts):
    context_text = "\n\n".join(
        f"(Page {c.get('page_start', 'N/A')}) {c['text']}"
        for c in contexts
    )

    return f"""
You are a Research Paper Management & analysis intelligence system assistant.
Answer ONLY using the context below.

Context:
{context_text}

Question:
{question}

Answer clearly and concisely.
"""


