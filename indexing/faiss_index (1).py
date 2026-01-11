import faiss
import numpy as np
import pickle
import os
from backend.indexing.embeddings import EmbeddingModel


class FAISSIndex:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.index = None
        self.chunks = []

    def index_papers(self, chunks):
        if not chunks:
            raise ValueError("No chunks provided")

        texts = [c["text"] for c in chunks]

        embeddings = self.embedding_model.embed_texts(texts)
        embeddings = np.array(embeddings).astype("float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.chunks = chunks  # store metadata

    def search(self, query, top_k=5):
        query_embedding = self.embedding_model.embed_texts([query])[0]
        query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                results.append({
                    **chunk,
                    "score": float(distances[0][rank])
                })

        return results

    def save(self, path="faiss_store"):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self, path="faiss_store"):
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)
