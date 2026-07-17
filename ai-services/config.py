import os
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ProviderConfig:
    name: str
    enabled: bool = True
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    default_model: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: float = 60.0


@dataclass
class AIConfig:
    app_name: str = "CrimeMatrix AI Services"
    version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8002

    # Provider configs
    ollama: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        name="ollama",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        default_model=os.getenv("OLLAMA_MODEL", "llama3.2:1b"),
    ))
    openai: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        default_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    ))
    gemini: ProviderConfig = field(default_factory=lambda: ProviderConfig(
        name="gemini",
        api_key=os.getenv("GEMINI_API_KEY", ""),
        default_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    ))

    # Agent defaults
    default_provider: str = "ollama"
    default_model: str = "llama3.2:1b"
    max_agent_steps: int = 10
    max_context_messages: int = 50

    # Token tracking
    track_tokens: bool = True

    # Streaming
    stream_chunk_size: int = 1024


def get_config() -> AIConfig:
    return AIConfig()
