import os
from typing import Dict, Optional


class PromptTemplate:
    def __init__(self, name: str, template: str, description: str = ""):
        self.name = name
        self.template = template
        self.description = description

    def render(self, **kwargs) -> str:
        result = self.template
        for key, value in kwargs.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result


class PromptManager:
    def __init__(self):
        self._templates: Dict[str, PromptTemplate] = {}
        self._load_defaults()

    def _load_defaults(self):
        self.register("system", PromptTemplate(
            name="system",
            template="You are a criminal intelligence copilot for the Karnataka State Police. You help officers analyze crimes, suspects, and investigations. Be precise, professional, and concise.",
            description="Default system prompt",
        ))
        self.register("criminal_analysis", PromptTemplate(
            name="criminal_analysis",
            template="Analyze the following criminal profile and provide insights on risk level, behavioral patterns, and recommended actions:\n\n{profile}",
            description="Criminal profile analysis",
        ))
        self.register("crime_summary", PromptTemplate(
            name="crime_summary",
            template="Summarize the following crime report concisely, highlighting key facts, suspects, and evidence:\n\n{report}",
            description="Crime report summary",
        ))
        self.register("graph_reasoning", PromptTemplate(
            name="graph_reasoning",
            template="Given the following network of relationships between suspects, evidence, and cases:\n\n{graph_data}\n\nAnalyze the connections and identify key patterns, accomplices, and potential leads.",
            description="Graph-based reasoning",
        ))

    def register(self, name: str, template: PromptTemplate):
        self._templates[name] = template

    def get(self, name: str) -> Optional[PromptTemplate]:
        return self._templates.get(name)

    def render(self, name: str, **kwargs) -> str:
        template = self._templates.get(name)
        if not template:
            raise ValueError(f"Prompt template '{name}' not found")
        return template.render(**kwargs)

    def list_all(self) -> list:
        return [
            {"name": t.name, "description": t.description}
            for t in self._templates.values()
        ]


prompt_manager = PromptManager()
