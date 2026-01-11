from backend.indexing.faiss_index import FAISSIndex
from backend.llm.groq_client import GroqLLM
from backend.rag.qa_pipeline import QAPipeline

faiss_index = FAISSIndex()
faiss_index.load("faiss_store")

llm = GroqLLM()
qa = QAPipeline(faiss_index, llm)

while True:
    q = input("\nAsk a question (or 'exit'): ")
    if q.lower() == "exit":
        break

    result = qa.ask(q)

    print("\nANSWER:\n", result["answer"])
    print("\nSOURCES:\n", result["sources"])
