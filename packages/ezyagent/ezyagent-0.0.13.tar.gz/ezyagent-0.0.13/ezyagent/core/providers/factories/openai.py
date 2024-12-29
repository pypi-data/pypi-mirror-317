from typing import Any
from openai import AsyncOpenAI,OpenAI
from ..base import ProviderFactory
from ..config import ProviderConfig

class OpenAIProviderFactory(ProviderFactory):
    """Factory for OpenAI provider"""
    def create_client(self, config: ProviderConfig, **kwargs: Any) -> OpenAI:
        return OpenAI(api_key=config.api_key, **kwargs)