from backend.rag.prompt_builder import build_prompt


class QAPipeline:
    def __init__(self, faiss_index, llm):
        self.index = faiss_index
        self.llm = llm

    def ask(self, question):
        retrieved = self.index.search(question, top_k=5)

        prompt = build_prompt(question, retrieved)
        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": self.format_sources(retrieved)
        }

    def format_sources(self, sources):
        lines = []
        for i, s in enumerate(sources, 1):
            lines.append(
                f"[{i}] Section: {s.get('section', 'N/A')} | "
                f"Page: {s.get('page_start', 'N/A')} | "
                f"Chunk ID: {s.get('chunk_id', 'N/A')}"
            )
        return "\n".join(lines)
