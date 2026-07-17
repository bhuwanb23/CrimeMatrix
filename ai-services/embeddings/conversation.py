from typing import List, Dict
from embeddings.base import DomainEmbedder
import numpy as np
import structlog

logger = structlog.get_logger()


class ConversationEmbeddings:
    def __init__(self):
        self.embedder = DomainEmbedder("conversation")

    def embed_turn(self, turn: Dict) -> list:
        text = f"{turn.get('role', '')} {turn.get('content', '')}"
        vec = self.embedder.embed_single(text)
        return vec.tolist()

    def embed_conversation(self, turns: List[Dict]) -> list:
        texts = [f"{t.get('role', '')} {t.get('content', '')}" for t in turns]
        if not self.embedder.is_fitted():
            self.embedder.fit(texts)
        vecs = self.embedder.embed(texts)
        return vecs.mean(axis=0).tolist()

    def similarity(self, t1: Dict, t2: Dict) -> float:
        v1 = np.array(self.embed_turn(t1))
        v2 = np.array(self.embed_turn(t2))
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10))
