from typing import Optional
from .openai_like import OpenAiApiLike
from requests.exceptions import RequestException


class OpenAIException(Exception):
    """Custom exception for OpenAI API errors"""
    pass


class OpenAIClient(OpenAiApiLike):
    """Client for interacting with OpenAI LLM API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
    ):
        if api_key is None:
            import os
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as OPENAI_API_KEY environment variable")

        super().__init__(api_key, "https://api.openai.com/v1")

    def _handle_request_exception(self, url: str, allow_one_retry: bool, e: RequestException):
        raise OpenAIException(
            f"API request failed: {str(e)}\nURL: {url}\nResponse: {e.response.text if hasattr(e, 'response') else 'No response'}")
