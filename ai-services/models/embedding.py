from typing import List, Dict, Optional
import numpy as np
from models.registry import model_registry
import structlog

logger = structlog.get_logger()

MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:
    def __init__(self):
        self._model = None
        self._dimension = 384

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(MODEL_NAME)
                self._dimension = self._model.get_sentence_embedding_dimension()
                logger.info("embedding_model_loaded", model=MODEL_NAME, dim=self._dimension)
            except Exception as e:
                logger.warning("embedding_model_fallback", error=str(e))
                self._model = "tfidf"
        return self._model

    async def embed(self, text: str, model: str = None) -> list:
        m = self._get_model()
        if m == "tfidf":
            from rag.embeddings import EmbeddingGenerator
            gen = EmbeddingGenerator()
            gen.fit([text])
            return gen.embed_single(text).tolist()
        vec = m.encode(text)
        return vec.tolist()

    async def embed_batch(self, texts: List[str], model: str = None) -> list:
        m = self._get_model()
        if m == "tfidf":
            from rag.embeddings import EmbeddingGenerator
            gen = EmbeddingGenerator()
            gen.fit(texts)
            return gen.embed(texts).tolist()
        vecs = m.encode(texts)
        return vecs.tolist()

    def similarity(self, vec1: list, vec2: list) -> float:
        a, b = np.array(vec1), np.array(vec2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    def get_config(self) -> Dict:
        m = self._get_model()
        return {
            "model": MODEL_NAME if m != "tfidf" else "tfidf_fallback",
            "dimension": self._dimension,
            "type": "sentence-transformers" if m != "tfidf" else "tfidf",
        }
