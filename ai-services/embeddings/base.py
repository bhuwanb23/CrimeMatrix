import numpy as np
from typing import List, Optional, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
import structlog

logger = structlog.get_logger()

DOMAIN_CONFIGS = {
    "fir": {"max_features": 3000, "ngram_range": (1, 2)},
    "evidence": {"max_features": 2000, "ngram_range": (1, 2)},
    "report": {"max_features": 5000, "ngram_range": (1, 3)},
    "conversation": {"max_features": 3000, "ngram_range": (1, 2)},
    "mo_fingerprint": {"max_features": 2000, "ngram_range": (1, 3)},
    "profile": {"max_features": 3000, "ngram_range": (1, 2)},
}


class DomainEmbedder:
    def __init__(self, domain: str, config: dict = None):
        self.domain = domain
        cfg = config or DOMAIN_CONFIGS.get(domain, {})
        self.vectorizer = TfidfVectorizer(
            max_features=cfg.get("max_features", 3000),
            ngram_range=cfg.get("ngram_range", (1, 2)),
            stop_words="english",
        )
        self._fitted = False
        self._dim = 0

    def fit(self, texts: List[str]):
        if not texts:
            return
        self.vectorizer.fit(texts)
        self._fitted = True
        self._dim = len(self.vectorizer.vocabulary_)

    def embed(self, texts: List[str]) -> np.ndarray:
        if not self._fitted:
            self.fit(texts)
        return self.vectorizer.transform(texts).toarray().astype(np.float32)

    def embed_single(self, text: str) -> np.ndarray:
        return self.embed([text])[0]

    def dimension(self) -> int:
        return self._dim

    def is_fitted(self) -> bool:
        return self._fitted
