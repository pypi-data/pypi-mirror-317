from typing import Optional
from .openai_like import OpenAiApiLike


class OllamaClient(OpenAiApiLike):
    """Client for interacting with OpenRouter LLM API"""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        api_key: Optional[str] = None,
    ):
        base_url = base_url[:-1] if base_url.endswith("/") else base_url
        super().__init__(api_key, f"{base_url}/v1")
