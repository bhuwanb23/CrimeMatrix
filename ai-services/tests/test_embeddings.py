import pytest
from embeddings.base import DomainEmbedder
from embeddings.store import EmbeddingStore
from embeddings.service import EmbeddingService
from embeddings.fir_embeddings import FIREmbeddings
from embeddings.evidence import EvidenceEmbeddings
from embeddings.profile import ProfileEmbeddings
from embeddings.mo_fingerprint import MOFingerprintEmbeddings
import numpy as np


class TestDomainEmbedder:
    def test_fit_and_embed(self):
        emb = DomainEmbedder("fir")
        texts = ["crime report theft", "murder investigation", "robbery case"]
        emb.fit(texts)
        vec = emb.embed_single("theft case")
        assert len(vec) > 0
        assert emb.is_fitted()

    def test_batch_embed(self):
        emb = DomainEmbedder("evidence")
        texts = ["cctv footage", "fingerprints found", "weapon recovered"]
        vecs = emb.embed(texts)
        assert vecs.shape[0] == 3


class TestEmbeddingStore:
    def test_add_and_get(self):
        store = EmbeddingStore()
        store.add("fir", "fir_1", [0.1, 0.2, 0.3], {"title": "Theft"})
        item = store.get("fir", "fir_1")
        assert item is not None
        assert item["id"] == "fir_1"

    def test_search(self):
        store = EmbeddingStore()
        store.add("fir", "fir_1", [1.0, 0.0, 0.0])
        store.add("fir", "fir_2", [0.9, 0.1, 0.0])
        store.add("fir", "fir_3", [0.0, 0.0, 1.0])
        results = store.search("fir", [1.0, 0.0, 0.0])
        assert results[0]["id"] == "fir_1"
        assert results[0]["score"] > 0.9

    def test_delete(self):
        store = EmbeddingStore()
        store.add("fir", "fir_1", [0.1, 0.2])
        assert store.delete("fir", "fir_1") is True
        assert store.get("fir", "fir_1") is None

    def test_stats(self):
        store = EmbeddingStore()
        store.add("fir", "fir_1", [0.1, 0.2, 0.3])
        store.add("evidence", "e_1", [0.1, 0.2])
        stats = store.get_stats()
        assert "fir" in stats
        assert stats["fir"]["count"] == 1

    def test_clear(self):
        store = EmbeddingStore()
        store.add("fir", "fir_1", [0.1])
        store.clear("fir")
        assert store.get("fir", "fir_1") is None


class TestFIREmbeddings:
    def test_embed_fir(self):
        fir = FIREmbeddings()
        vec = fir.embed_fir({"title": "Theft at MG Road", "description": "Stolen jewelry", "crime_type": "theft"})
        assert len(vec) > 0

    def test_similarity(self):
        fir = FIREmbeddings()
        score = fir.similarity(
            {"title": "Theft at MG Road", "description": "Jewelry stolen"},
            {"title": "Theft at MG Road", "description": "Gold stolen"},
        )
        assert score > 0.3


class TestEvidenceEmbeddings:
    def test_embed_evidence(self):
        ev = EvidenceEmbeddings()
        vec = ev.embed_evidence({"title": "CCTV footage", "description": "Shows suspect", "type": "physical"})
        assert len(vec) > 0


class TestProfileEmbeddings:
    def test_embed_profile(self):
        prof = ProfileEmbeddings()
        vec = prof.embed_profile({"name": "John", "description": "Known thief", "district": "Bangalore"})
        assert len(vec) > 0

    def test_similarity(self):
        prof = ProfileEmbeddings()
        score = prof.similarity(
            {"name": "John", "description": "Known thief"},
            {"name": "Johnny", "description": "Known robber"},
        )
        assert score > 0.2


class TestMOFingerprint:
    def test_embed_mo(self):
        mo = MOFingerprintEmbeddings()
        vec = mo.embed_mo({"description": "Broke window at night, stole jewelry"})
        assert len(vec) > 0

    def test_find_similar(self):
        mo = MOFingerprintEmbeddings()
        candidates = [
            {"case_id": 1, "description": "Broke door at night, stole cash"},
            {"case_id": 2, "description": "Con artist tricked victim"},
        ]
        results = mo.find_similar({"description": "Broke window at night"}, candidates)
        assert results[0]["case_id"] == 1


class TestEmbeddingService:
    def setup_method(self):
        self.service = EmbeddingService()

    @pytest.mark.asyncio
    async def test_embed(self):
        vec = await self.service.embed("Theft at MG Road", "fir", "fir_1")
        assert len(vec) > 0

    @pytest.mark.asyncio
    async def test_embed_stores(self):
        await self.service.embed("Test", "fir", "fir_test")
        item = self.service.store.get("fir", "fir_test")
        assert item is not None

    @pytest.mark.asyncio
    async def test_search(self):
        await self.service.embed("Theft case", "fir", "fir_1")
        await self.service.embed("Robbery case", "fir", "fir_2")
        results = await self.service.search("theft", "fir")
        assert len(results) > 0

    def test_similarity(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.9, 0.1, 0.0]
        score = self.service.similarity(v1, v2)
        assert score > 0.8

    def test_stats(self):
        stats = self.service.get_stats()
        assert "domains" in stats
        assert len(stats["domains"]) == 6
