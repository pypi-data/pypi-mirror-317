from typing import Optional
from .openai_like import OpenAiApiLike


class OpenRouterClient(OpenAiApiLike):
    """Client for interacting with OpenRouter LLM API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
    ):
        if api_key is None:
            import os
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as OPENROUTER_API_KEY environment variable")

        super().__init__(api_key, "https://openrouter.ai/api/v1")
