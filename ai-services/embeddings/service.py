from typing import Dict, List, Optional
from embeddings.base import DomainEmbedder
from embeddings.store import EmbeddingStore
from embeddings.fir_embeddings import FIREmbeddings
from embeddings.evidence import EvidenceEmbeddings
from embeddings.report import ReportEmbeddings
from embeddings.conversation import ConversationEmbeddings
from embeddings.mo_fingerprint import MOFingerprintEmbeddings
from embeddings.profile import ProfileEmbeddings
import structlog

logger = structlog.get_logger()


class EmbeddingService:
    def __init__(self):
        self.store = EmbeddingStore()
        self.fir = FIREmbeddings()
        self.evidence = EvidenceEmbeddings()
        self.report = ReportEmbeddings()
        self.conversation = ConversationEmbeddings()
        self.mo = MOFingerprintEmbeddings()
        self.profile = ProfileEmbeddings()
        self._domain_map = {
            "fir": self.fir,
            "evidence": self.evidence,
            "report": self.report,
            "conversation": self.conversation,
            "mo_fingerprint": self.mo,
            "profile": self.profile,
        }

    async def embed(self, text: str, domain: str = "fir", item_id: str = None) -> list:
        embedder = self._domain_map.get(domain)
        if embedder:
            data = {"title": text, "description": "", "content": text, "text": text}
            if hasattr(embedder, 'embed_fir'):
                vec = embedder.embed_fir(data)
            elif hasattr(embedder, 'embed_evidence'):
                vec = embedder.embed_evidence(data)
            elif hasattr(embedder, 'embed_report'):
                vec = embedder.embed_report(data)
            elif hasattr(embedder, 'embed_turn'):
                vec = embedder.embed_turn({"role": "user", "content": text})
            elif hasattr(embedder, 'embed_mo'):
                vec = embedder.embed_mo({"description": text})
            elif hasattr(embedder, 'embed_profile'):
                vec = embedder.embed_profile({"name": text, "description": text})
            else:
                vec = []
        else:
            vec = []

        if vec and item_id:
            self.store.add(domain, item_id, vec, {"text": text[:200]})
        return vec

    async def embed_batch(self, texts: List[str], domain: str = "fir") -> list:
        embedder = self._domain_map.get(domain)
        if not embedder:
            return []

        if hasattr(embedder, 'embed_batch'):
            data = [{"title": t, "description": "", "content": t} for t in texts]
            return embedder.embed_batch(data)
        return []

    def similarity(self, vec1: list, vec2: list) -> float:
        import numpy as np
        a, b = np.array(vec1), np.array(vec2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    async def search(self, text: str, domain: str = "fir", top_k: int = 5) -> List[Dict]:
        vec = await self.embed(text, domain)
        if not vec:
            return []
        return self.store.search(domain, vec, top_k)

    def get_stats(self) -> dict:
        return {
            "domains": list(self._domain_map.keys()),
            "store": self.store.get_stats(),
        }
