from typing import List, Dict, Optional
import numpy as np
from rag.embeddings import EmbeddingGenerator
from models.registry import model_registry
import structlog

logger = structlog.get_logger()


class EmbeddingModel:
    def __init__(self):
        self._generators: Dict[str, EmbeddingGenerator] = {}
        self._default = "tfidf"

    def _get_generator(self, name: str = None) -> EmbeddingGenerator:
        name = name or self._default
        if name not in self._generators:
            self._generators[name] = EmbeddingGenerator()
        return self._generators[name]

    async def embed(self, text: str, model: str = None) -> list:
        gen = self._get_generator(model)
        vec = gen.embed_single(text)
        return vec.tolist()

    async def embed_batch(self, texts: List[str], model: str = None) -> list:
        gen = self._get_generator(model)
        if not gen._fitted:
            gen.fit(texts)
        vecs = gen.embed(texts)
        return vecs.tolist()

    def similarity(self, vec1: list, vec2: list) -> float:
        a, b = np.array(vec1), np.array(vec2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    def get_config(self) -> Dict:
        return {
            "default_model": model_registry.get_model_name("embedding") or self._default,
            "available": ["tfidf"],
        }
