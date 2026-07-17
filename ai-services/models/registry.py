from typing import Dict, List, Optional
import structlog

logger = structlog.get_logger()

MODEL_TYPES = ["conversation", "embedding", "speech", "translation", "prediction"]


class ModelConfig:
    def __init__(self, name: str, model_type: str, provider: str,
                 model_name: str = None, config: dict = None):
        self.name = name
        self.model_type = model_type
        self.provider = provider
        self.model_name = model_name
        self.config = config or {}

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.model_type,
            "provider": self.provider,
            "model": self.model_name,
            "config": self.config,
        }


class ModelRegistry:
    def __init__(self):
        self._models: Dict[str, Dict[str, ModelConfig]] = {t: {} for t in MODEL_TYPES}
        self._defaults: Dict[str, str] = {}

    def register(self, name: str, model_type: str, provider: str,
                 model_name: str = None, config: dict = None, default: bool = False):
        if model_type not in self._models:
            self._models[model_type] = {}
        mc = ModelConfig(name, model_type, provider, model_name, config)
        self._models[model_type][name] = mc
        if default or model_type not in self._defaults:
            self._defaults[model_type] = name
        logger.info("model_registered", name=name, type=model_type, provider=provider)

    def get(self, model_type: str, name: str = None) -> Optional[ModelConfig]:
        name = name or self._defaults.get(model_type)
        return self._models.get(model_type, {}).get(name)

    def get_provider(self, model_type: str, name: str = None) -> str:
        mc = self.get(model_type, name)
        return mc.provider if mc else None

    def get_model_name(self, model_type: str, name: str = None) -> Optional[str]:
        mc = self.get(model_type, name)
        return mc.model_name if mc else None

    def list_type(self, model_type: str) -> List[Dict]:
        return [mc.to_dict() for mc in self._models.get(model_type, {}).values()]

    def list_all(self) -> Dict[str, List[Dict]]:
        return {t: self.list_type(t) for t in MODEL_TYPES}

    def set_default(self, model_type: str, name: str):
        if name in self._models.get(model_type, {}):
            self._defaults[model_type] = name

    def get_defaults(self) -> Dict[str, str]:
        return dict(self._defaults)

    def remove(self, model_type: str, name: str) -> bool:
        if name in self._models.get(model_type, {}):
            del self._models[model_type][name]
            if self._defaults.get(model_type) == name:
                remaining = list(self._models[model_type].keys())
                self._defaults[model_type] = remaining[0] if remaining else None
            return True
        return False


model_registry = ModelRegistry()
