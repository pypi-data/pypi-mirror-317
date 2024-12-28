from typing import List, Optional, Union, Generator
import requests
from abc import ABC, abstractmethod


class BaseClient(ABC):
    """Abstract base class for LLM clients"""

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/') if base_url else None
        if base_url:
            self.session = requests.Session()
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })

    @abstractmethod
    def chat_completion(
        self,
        messages: List,
        model: str,
        system: Optional[str] = None,
        response_type: type = str,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        prompt_template: Optional[str] = None,
        max_retries: int = 0,
        fallback_client=None,
        **kwargs
    ) -> Union[str, dict, Generator]:
        """Generate chat completion using the provider's API"""
        pass

    @abstractmethod
    def _handle_request_exception(self, url: str, allow_one_retry: bool, e: Exception):
        """Handle provider-specific request exceptions"""
        pass
