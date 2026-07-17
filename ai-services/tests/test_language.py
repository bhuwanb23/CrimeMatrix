import pytest
from language.stt import SpeechToText
from language.tts import TextToSpeech
from language.translator import Translator
from language.kanglish import KanglishNormalizer
from language.normalizer import QueryNormalizer


class TestSpeechToText:
    def setup_method(self):
        self.stt = SpeechToText()

    @pytest.mark.asyncio
    async def test_transcribe_text(self):
        result = await self.stt.transcribe(audio_text="Hello world")
        assert result["text"] == "Hello world"
        assert result["language"] == "en"

    @pytest.mark.asyncio
    async def test_detect_kannada(self):
        result = await self.stt.transcribe(audio_text="ಕನ್ನಡ ಭಾಷೆ")
        assert result["language"] == "kn"

    @pytest.mark.asyncio
    async def test_no_input(self):
        result = await self.stt.transcribe()
        assert result["text"] == ""

    def test_formats(self):
        assert "wav" in self.stt.get_supported_formats()


class TestTextToSpeech:
    def setup_method(self):
        self.tts = TextToSpeech()

    @pytest.mark.asyncio
    async def test_synthesize(self):
        result = await self.tts.synthesize("Hello world")
        assert "ssml" in result
        assert "Hello world" in result["ssml"]

    @pytest.mark.asyncio
    async def test_kannada_voice(self):
        result = await self.tts.synthesize("ನಮಸ್ಕಾರ", language="kn")
        assert result["language"] == "kn"
        assert "kn-IN" in result["ssml"]

    def test_voices(self):
        voices = self.tts.get_voices()
        assert "en" in voices
        assert "kn" in voices


class TestTranslator:
    def setup_method(self):
        self.translator = Translator()

    def test_en_to_kn(self):
        result = self.translator.translate("hello", "en", "kn")
        assert result["translated"] == "ನಮಸ್ಕಾರ"

    def test_kn_to_en(self):
        result = self.translator.translate("ಪೊಲೀಸ್", "kn", "en")
        assert result["translated"] == "police"

    def test_auto_detect(self):
        result = self.translator.translate("ಕಳ್ಳತನ", "auto", "en")
        assert result["translated"] == "theft"

    def test_same_lang(self):
        result = self.translator.translate("hello", "en", "en")
        assert result["translated"] == "hello"

    def test_batch(self):
        results = self.translator.batch_translate(["hello", "police"], "en", "kn")
        assert len(results) == 2
        assert results[0]["translated"] == "ನಮಸ್ಕಾರ"


class TestKanglishNormalizer:
    def setup_method(self):
        self.kn = KanglishNormalizer()

    def test_to_english(self):
        result = self.kn.normalize("namaskara howdu", "english")
        assert result["normalized"] == "hello yes"

    def test_to_kannada(self):
        result = self.kn.normalize("hello police", "kannada")
        assert "ನಮಸ್ಕಾರ" in result["normalized"]

    def test_detect_kanglish(self):
        result = self.kn.normalize("namaskara")
        assert result["is_kanglish"] is True

    def test_detect_script_english(self):
        assert self.kn.detect_script("hello world") == "english"

    def test_detect_script_kannada(self):
        assert self.kn.detect_script("ಕನ್ನಡ") == "kannada"

    def test_detect_script_kanglish(self):
        assert self.kn.detect_script("namaskara") == "kanglish"


class TestQueryNormalizer:
    def setup_method(self):
        self.norm = QueryNormalizer()

    def test_basic_normalize(self):
        result = self.norm.normalize("Theft near bengaluru!!!")
        assert result["normalized"] == "theft bengaluru"

    def test_stop_words(self):
        result = self.norm.normalize("what is the crime in bangalore")
        assert "is" not in result["normalized"]
        assert "the" not in result["normalized"]

    def test_kanglish_auto(self):
        result = self.norm.normalize("howdu polisi")
        assert result["kanglish_detected"] is True

    def test_synonym_expansion(self):
        result = self.norm.normalize("robbery case")
        assert "steal" in result["expanded"] or "theft" in result["expanded"]

    def test_batch(self):
        results = self.norm.batch_normalize(["theft case", "murder report"])
        assert len(results) == 2
