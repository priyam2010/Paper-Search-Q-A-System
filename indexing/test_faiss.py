from backend.ingestion.paper_ingestor import ingest_paper
from backend.indexing.chunk_builder import build_chunks
from backend.indexing.faiss_index import FAISSIndex


if __name__ == "__main__":
    # 1. Ingest paper
    paper = ingest_paper("data/standard-treatment-guidelines.pdf")

    # 2. Build chunks (THIS WAS THE MISSING LINK)
    chunks = build_chunks(paper)

    print("TOTAL CHUNKS PASSED TO FAISS:", len(chunks))

    # 3. Index chunks
    faiss_index = FAISSIndex()
    faiss_index.index_papers(chunks)

    # 4. Simple search test
    results = faiss_index.semantic_search(
        query="What is the purpose of standard treatment guidelines?",
        top_k=3
    )

    for r in results:
        print("\nSECTION:", r["metadata"]["section"])
        print(r["text"][:500])
