from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_chunks(pages, chunk_size=500, overlap=100):
    chunks = []

    for page in pages:
        text = page["text"]
        page_num = page["page"]

        start = 0
        while start < len(text):
            chunk_text = text[start:start + chunk_size]

            chunks.append({
                "text": chunk_text,
                "page_start": page_num,
                "page_end": page_num
            })

            start += chunk_size - overlap

    return chunks


    print(f"✅ Page-aware chunks built: {len(chunks)}")
    return chunks

