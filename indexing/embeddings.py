from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_texts(self, texts: List[str]):
        """
        Embed a list of texts (used for indexing)
        """
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, query: str):
        """
        Embed a single query (used for search)
        """
        return self.model.encode([query])[0]
