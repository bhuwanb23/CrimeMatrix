from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger()


class WorkflowState:
    def __init__(self, initial: Dict = None):
        self._data: Dict[str, Any] = initial or {}
        self._step_results: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        return dict(self._data)

    def set_step_result(self, step_name: str, result: Any):
        self._step_results[step_name] = result
        self._data[f"step_{step_name}"] = result

    def get_step_result(self, step_name: str) -> Any:
        return self._step_results.get(step_name)

    def clear(self):
        self._data.clear()
        self._step_results.clear()
