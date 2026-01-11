class Retriever:
    def __init__(self, faiss_index):
        self.index = faiss_index

    def retrieve(self, query: str, k=5):
        results = self.index.search(query, top_k=k)
        return [r["text"] for r in results]
