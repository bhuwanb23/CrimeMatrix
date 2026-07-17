import pytest
from models.registry import ModelRegistry, ModelConfig, MODEL_TYPES
from models.conversation import ConversationModel
from models.embedding import EmbeddingModel
from models.speech import SpeechModel
from models.translation import TranslationModel
from models.prediction import PredictionModel


class TestModelRegistry:
    def setup_method(self):
        self.reg = ModelRegistry()

    def test_register_and_get(self):
        self.reg.register("gpt4", "conversation", "openai", "gpt-4")
        mc = self.reg.get("conversation", "gpt4")
        assert mc is not None
        assert mc.provider == "openai"

    def test_default(self):
        self.reg.register("ollama", "conversation", "ollama", "llama3.2:1b", default=True)
        mc = self.reg.get("conversation")
        assert mc.name == "ollama"

    def test_list_type(self):
        self.reg.register("m1", "conversation", "openai")
        self.reg.register("m2", "conversation", "ollama")
        models = self.reg.list_type("conversation")
        assert len(models) == 2

    def test_list_all(self):
        self.reg.register("m1", "conversation", "openai")
        self.reg.register("m2", "embedding", "tfidf")
        all_models = self.reg.list_all()
        assert "conversation" in all_models
        assert "embedding" in all_models

    def test_remove(self):
        self.reg.register("m1", "conversation", "openai")
        assert self.reg.remove("conversation", "m1") is True
        assert self.reg.get("conversation", "m1") is None

    def test_remove_nonexistent(self):
        assert self.reg.remove("conversation", "nonexistent") is False

    def test_set_default(self):
        self.reg.register("m1", "conversation", "openai")
        self.reg.register("m2", "conversation", "ollama")
        self.reg.set_default("conversation", "m2")
        mc = self.reg.get("conversation")
        assert mc.name == "m2"

    def test_get_provider(self):
        self.reg.register("m1", "conversation", "openai", "gpt-4")
        provider = self.reg.get_provider("conversation", "m1")
        assert provider == "openai"

    def test_get_model_name(self):
        self.reg.register("m1", "conversation", "openai", "gpt-4")
        model_name = self.reg.get_model_name("conversation", "m1")
        assert model_name == "gpt-4"

    def test_model_types(self):
        assert "conversation" in MODEL_TYPES
        assert "embedding" in MODEL_TYPES
        assert "speech" in MODEL_TYPES
        assert "translation" in MODEL_TYPES
        assert "prediction" in MODEL_TYPES


class TestModelConfig:
    def test_to_dict(self):
        mc = ModelConfig("gpt4", "conversation", "openai", "gpt-4", {"temp": 0.7})
        d = mc.to_dict()
        assert d["name"] == "gpt4"
        assert d["provider"] == "openai"


class TestConversationModel:
    def setup_method(self):
        self.model = ConversationModel()

    def test_config(self):
        config = self.model.get_config()
        assert "provider" in config
        assert "model" in config


class TestEmbeddingModel:
    def setup_method(self):
        self.model = EmbeddingModel()

    @pytest.mark.asyncio
    async def test_embed(self):
        vec = await self.model.embed("hello world")
        assert len(vec) > 0

    @pytest.mark.asyncio
    async def test_embed_batch(self):
        vecs = await self.model.embed_batch(["hello", "world"])
        assert len(vecs) == 2

    def test_similarity(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.9, 0.1, 0.0]
        score = self.model.similarity(v1, v2)
        assert score > 0.8

    def test_config(self):
        config = self.model.get_config()
        assert "model" in config


class TestSpeechModel:
    def setup_method(self):
        self.model = SpeechModel()

    @pytest.mark.asyncio
    async def test_transcribe(self):
        result = await self.model.transcribe(audio_text="hello")
        assert result["text"] == "hello"

    @pytest.mark.asyncio
    async def test_synthesize(self):
        result = await self.model.synthesize("hello world")
        assert "ssml" in result

    def test_config(self):
        config = self.model.get_config()
        assert "supported_languages" in config


class TestTranslationModel:
    def setup_method(self):
        self.model = TranslationModel()

    @pytest.mark.asyncio
    async def test_translate(self):
        result = await self.model.translate("hello", "en", "kn")
        assert result["translated"] == "ನಮಸ್ಕಾರ"

    @pytest.mark.asyncio
    async def test_kanglish(self):
        result = await self.model.kanglish_normalize("namaskara")
        assert result["is_kanglish"] is True

    def test_config(self):
        config = self.model.get_config()
        assert "supported_pairs" in config


class TestPredictionModel:
    def setup_method(self):
        self.model = PredictionModel()

    @pytest.mark.asyncio
    async def test_predict(self):
        result = await self.model.predict("risk", {"profile": {"prior_offenses": 3}})
        assert "risk_score" in result

    def test_config(self):
        config = self.model.get_config()
        assert "available_types" in config
