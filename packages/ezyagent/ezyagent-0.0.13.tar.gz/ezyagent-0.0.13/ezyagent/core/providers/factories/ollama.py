from typing import Any
from openai import OpenAI
from ..base import ProviderFactory
from ..config import ProviderConfig

class OllamaProviderFactory(ProviderFactory):
    """Factory for Ollama provider"""
    def create_client(self, config: ProviderConfig, **kwargs: Any) -> OpenAI:
        base_url = config.base_url or 'http://localhost:11434/v1'
        api_key = config.api_key or 'ollama'
        return OpenAI(base_url=base_url, api_key=api_key, **kwargs)