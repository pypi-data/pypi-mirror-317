from typing import Any
from openai import OpenAI
from ..base import ProviderFactory
from ..config import ProviderConfig

class HuggingFaceProviderFactory(ProviderFactory):
    """Factory for HuggingFace provider"""
    def create_client(self, config: ProviderConfig, **kwargs: Any) -> OpenAI:
        base_url = config.base_url or 'https://api-inference.huggingface.co/v1/'
        return OpenAI(base_url=base_url, api_key=config.api_key, **kwargs)