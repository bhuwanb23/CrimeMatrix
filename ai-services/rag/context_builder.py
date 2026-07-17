from typing import List


class RAGContextBuilder:
    def build(self, query: str, results: list) -> str:
        if not results:
            return f"No relevant documents found for: {query}"

        parts = [f"## Retrieved Context for: {query}\n"]
        for i, r in enumerate(results):
            score = r.get("score", 0)
            doc_type = r.get("doc_type", "unknown")
            source = r.get("source", "")
            content = r.get("content", "")[:500]

            parts.append(f"### Source {i+1} [{doc_type}] (relevance: {score:.3f})")
            parts.append(f"- Source: {source}")
            parts.append(f"- Content: {content}")
            parts.append("")

        parts.append("---")
        parts.append(f"Found {len(results)} relevant sources. Use this information to answer the user's query.")

        return "\n".join(parts)

    def build_citations(self, results: list) -> list:
        citations = []
        for i, r in enumerate(results):
            citations.append({
                "index": i + 1,
                "doc_id": r.get("doc_id", ""),
                "doc_type": r.get("doc_type", ""),
                "source": r.get("source", ""),
                "score": round(r.get("score", 0), 3),
                "excerpt": r.get("content", "")[:200],
            })
        return citations
