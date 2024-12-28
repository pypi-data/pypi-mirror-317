from typing import List, Optional
from requests.exceptions import RequestException
import json

from .openai_like import OpenAiApiLike

import logging
logger = logging.getLogger(__name__)


class GroqApiException(Exception):
    """Custom exception for Groq API errors"""
    pass


class GroqClient(OpenAiApiLike):
    """Client for interacting with Groq's LLM API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
    ):
        if api_key is None:
            import os
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as GROQ_API_KEY environment variable")

        super().__init__(api_key, "https://api.groq.com/openai/v1")

    def _handle_request_exception(self, url: str, allow_one_retry: bool, e: RequestException):
        import re
        import math
        import time

        error_values = json.loads(e.response.text)
        text = error_values["error"]["message"]

        if "rate limit" in text.lower() and allow_one_retry:
            pattern = r"try again in (\d+\.?\d*)s"
            match = re.search(pattern, text)
            if match:
                seconds = math.ceil(float(match.group(1)))
                time.sleep(seconds + 1)
                return
        raise GroqApiException(
            f"API request failed: {str(e)}\nURL: {url}\nResponse: {e.response.text if hasattr(e, 'response') else 'No response'}")
