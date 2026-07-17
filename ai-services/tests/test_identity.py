import pytest
from identity.name_matcher import IndianNameMatcher
from identity.transliteration import TransliterationEngine
from identity.duplicate_detector import DuplicateDetector
from identity.entity_resolver import EntityResolver
from identity.record_merger import RecordMerger
from identity.alias_detector import AliasDetector


class TestIndianNameMatcher:
    def setup_method(self):
        self.matcher = IndianNameMatcher()

    def test_exact_match(self):
        result = self.matcher.match("Rajesh Kumar", "Rajesh Kumar")
        assert result["score"] == 100

    def test_case_insensitive(self):
        result = self.matcher.match("RAJESH KUMAR", "rajesh kumar")
        assert result["score"] == 100

    def test_nickname_rajesh(self):
        result = self.matcher.match("Raj", "Rajesh")
        assert result["score"] >= 70
        assert result["match_type"] == "nickname"

    def test_nickname_ram(self):
        result = self.matcher.match("Ram", "Ramesh")
        assert result["score"] >= 70

    def test_partial_match(self):
        result = self.matcher.match("Rajesh Kumar", "Rajesh Singh")
        assert result["score"] > 50

    def test_no_match(self):
        result = self.matcher.match("Rajesh", "Suresh Patel")
        assert result["score"] < 50

    def test_surname_match(self):
        result = self.matcher.match("Rajesh Kumar", "Suresh Kumar")
        assert result["score"] > 40

    def test_batch_match(self):
        results = self.matcher.batch_match("Raj", ["Rajesh", "Suresh", "Raju"], threshold=50)
        assert len(results) >= 1
        assert results[0]["name"] in ["Rajesh", "Raju"]

    def test_single_name(self):
        result = self.matcher.match("Kumar", "Kumar")
        assert result["score"] == 100


class TestTransliterationEngine:
    def setup_method(self):
        self.engine = TransliterationEngine()

    def test_detect_latin(self):
        assert self.engine.detect_script("Hello") == "latin"

    def test_detect_kannada(self):
        assert self.engine.detect_script("ಕನ್ನಡ") == "kannada"

    def test_detect_devanagari(self):
        assert self.engine.detect_script("हिन्दी") == "devanagari"

    def test_kannada_to_english(self):
        result = self.engine.transliterate("ಕನ್ನಡ", "english")
        assert result["script"] == "kannada"
        assert len(result["result"]) > 0

    def test_devanagari_to_english(self):
        result = self.engine.transliterate("हिन्दी", "english")
        assert result["script"] == "devanagari"
        assert len(result["result"]) > 0

    def test_english_to_kannada(self):
        result = self.engine.transliterate("kannada", "kannada")
        assert result["target"] == "kannada"
        assert len(result["result"]) > 0

    def test_latin_passthrough(self):
        result = self.engine.transliterate("Hello", "english")
        assert result["result"] == "Hello"


class TestDuplicateDetector:
    def setup_method(self):
        self.detector = DuplicateDetector()

    def test_exact_name_duplicates(self):
        records = [
            {"id": 1, "name": "Rajesh Kumar", "age": 30},
            {"id": 2, "name": "Rajesh Kumar", "age": 30},
        ]
        dups = self.detector.find_duplicates(records)
        assert len(dups) == 1
        assert dups[0]["score"] == 100

    def test_phone_duplicates(self):
        records = [
            {"id": 1, "name": "Rajesh", "phone": "9876543210"},
            {"id": 2, "name": "Raj", "phone": "9876543210"},
        ]
        dups = self.detector.find_duplicates(records)
        assert len(dups) == 1

    def test_no_duplicates(self):
        records = [
            {"id": 1, "name": "Rajesh Kumar", "age": 30},
            {"id": 2, "name": "Suresh Patel", "age": 45},
        ]
        dups = self.detector.find_duplicates(records)
        assert len(dups) == 0

    def test_nickname_duplicates(self):
        records = [
            {"id": 1, "name": "Rajesh Kumar"},
            {"id": 2, "name": "Raj Kumar"},
        ]
        dups = self.detector.find_duplicates(records)
        assert len(dups) == 1


class TestEntityResolver:
    def setup_method(self):
        self.resolver = EntityResolver()

    def test_resolve_person(self):
        candidates = [
            {"id": 1, "name": "Rajesh Kumar"},
            {"id": 2, "name": "Suresh Patel"},
        ]
        result = self.resolver.resolve_person("Rajesh", candidates)
        assert result is not None
        assert result["id"] == 1

    def test_resolve_from_text(self):
        entities = [
            {"id": 1, "name": "Rajesh Kumar"},
            {"id": 2, "name": "Suresh Patel"},
        ]
        results = self.resolver.resolve_from_text("Tell me about Rajesh Kumar", entities)
        assert len(results) > 0

    def test_suggest_entity(self):
        candidates = [
            {"id": 1, "name": "Rajesh Kumar"},
            {"id": 2, "name": "Rajendra Singh"},
        ]
        suggestions = self.resolver.suggest_entity("Raj", candidates)
        assert len(suggestions) > 0


class TestRecordMerger:
    def setup_method(self):
        self.merger = RecordMerger()

    def test_merge(self):
        primary = {"id": 1, "name": "Rajesh", "age": 30, "phone": "123"}
        secondary = {"id": 2, "name": "Rajesh Kumar", "age": 30, "district": "Bangalore"}
        merged = self.merger.merge(primary, secondary)
        assert merged["name"] == "Rajesh Kumar"
        assert merged["district"] == "Bangalore"

    def test_merge_preserves_primary(self):
        primary = {"id": 1, "name": "Rajesh", "phone": "123"}
        secondary = {"id": 2, "name": "Raj", "phone": "456"}
        merged = self.merger.merge(primary, secondary)
        assert merged["id"] == 1
        assert merged["phone"] == "123"

    def test_merge_log(self):
        primary = {"id": 1, "name": "A"}
        secondary = {"id": 2, "name": "B"}
        self.merger.merge(primary, secondary)
        log = self.merger.get_merge_log()
        assert len(log) == 1

    def test_suggest_best_fields(self):
        records = [
            {"name": "Raj", "phone": "123"},
            {"name": "Rajesh Kumar", "phone": "12345"},
        ]
        best = self.merger.suggest_best_fields(records)
        assert best["name"] == "Rajesh Kumar"
        assert best["phone"] == "12345"


class TestAliasDetector:
    def setup_method(self):
        self.detector = AliasDetector()

    def test_known_aliases(self):
        aliases = self.detector.detect_aliases("Rajesh Kumar", known_aliases=["Raj", "RK"])
        assert len(aliases) >= 2

    def test_nickname_detection(self):
        aliases = self.detector.detect_aliases("Rajesh", all_names=["Raj", "Raju", "Suresh"])
        assert len(aliases) > 0

    def test_title_detection(self):
        aliases = self.detector.detect_aliases("Rajesh bhai")
        title_aliases = [a for a in aliases if a["type"] == "title"]
        assert len(title_aliases) > 0

    def test_suggest_aliases(self):
        suggestions = self.detector.suggest_aliases("Raj")
        assert len(suggestions) > 0
        assert "rajesh" in suggestions or "rajendra" in suggestions
