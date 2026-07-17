from typing import List
from rag.document import Document


class TextChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: Document) -> List[dict]:
        text = document.content
        if len(text) <= self.chunk_size:
            return [{
                "chunk_id": f"{document.doc_id}_0",
                "content": text,
                "doc_id": document.doc_id,
                "doc_type": document.doc_type,
                "metadata": document.metadata,
                "source": document.source,
                "chunk_index": 0,
            }]

        chunks = []
        start = 0
        idx = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            chunks.append({
                "chunk_id": f"{document.doc_id}_{idx}",
                "content": chunk_text,
                "doc_id": document.doc_id,
                "doc_type": document.doc_type,
                "metadata": document.metadata,
                "source": document.source,
                "chunk_index": idx,
            })
            start += self.chunk_size - self.chunk_overlap
            idx += 1
        return chunks

    def chunk_all(self, documents: List[Document]) -> List[dict]:
        all_chunks = []
        for doc in documents:
            all_chunks.extend(self.chunk(doc))
        return all_chunks
