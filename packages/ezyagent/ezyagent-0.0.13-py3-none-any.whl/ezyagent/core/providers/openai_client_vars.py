from openai import OpenAI
from typing import Optional, Mapping, Any
import httpx


class OllamaOpenAI(OpenAI):
    def __init__(
        self,
        *,
        model: Optional[str] = "qwen2.5:3b-instruct",
        base_url: str | httpx.URL | None = "http://localhost:11434/v1",
        api_key: str | None = "ollama",
        organization: str | None = None,
        project: str | None = None,
        timeout: float | None = None,
        max_retries: int = 2,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        **kwargs: Any
    ) -> None:
        # Store the model parameter for use in API calls
        self.model = model

        super().__init__(
            api_key=api_key,
            organization=organization,
            project=project,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            **kwargs
        )


class HFOpenAI(OpenAI):
    def __init__(
        self,
        *,
        model: Optional[str] = None,
        base_url: str | httpx.URL | None = "https://api-inference.huggingface.co/v1",
        api_key: str | None = "your-hf-token",
        organization: str | None = None,
        project: str | None = None,
        timeout: float | None = None,
        max_retries: int = 2,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        **kwargs: Any
    ) -> None:
        # Store the model parameter for use in API calls
        self.model = model

        super().__init__(
            api_key=api_key,
            organization=organization,
            project=project,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            **kwargs
        )