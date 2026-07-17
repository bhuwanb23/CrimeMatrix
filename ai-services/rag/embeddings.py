import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
import structlog

logger = structlog.get_logger()


class EmbeddingGenerator:
    def __init__(self, max_features: int = 5000):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words="english",
            ngram_range=(1, 2),
        )
        self._fitted = False
        self._vocabulary_size = 0

    def fit(self, texts: List[str]):
        if not texts:
            return
        self.vectorizer.fit(texts)
        self._fitted = True
        self._vocabulary_size = len(self.vectorizer.vocabulary_)
        logger.info("embeddings_fitted", vocab_size=self._vocabulary_size, docs=len(texts))

    def embed(self, texts: List[str]) -> np.ndarray:
        if not self._fitted:
            self.fit(texts)
        return self.vectorizer.transform(texts).toarray().astype(np.float32)

    def embed_single(self, text: str) -> np.ndarray:
        return self.embed([text])[0]

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
