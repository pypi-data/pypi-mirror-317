from typing import List, Optional, Union, Generator, Callable
import google.generativeai as genai

from pulsar.parser import parse
from pulsar.prompt import build_prompt, DEFAULT_PROMPT

from .base import BaseClient


class GeminiException(Exception):
    """Custom exception for Gemini API errors"""
    pass


class GeminiClient(BaseClient):
    """Client for interacting with Google's Gemini API"""

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            import os
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as GOOGLE_API_KEY environment variable")

        super().__init__(api_key, None)
        genai.configure(api_key=api_key)

    def _handle_request_exception(self, url: str, allow_one_retry: bool, e: Exception):
        raise GeminiException(f"Gemini API request failed: {str(e)}")

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
        try:
            model = genai.GenerativeModel(model)
            chat = model.start_chat(history=[])

            if system:
                chat.send_message(system)

            for message in messages:
                chat.send_message(message["content"])

            response = chat.send_message(
                "",
                stream=stream,
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )

            if stream:
                def stream_generator():
                    for chunk in response:
                        yield chunk.text
                return stream_generator()

            response_content = response.text
            if response_type == str:
                return response_content
            return parse(response_content, response_type)

        except Exception as e:
            if fallback_client and max_retries > 0:
                return fallback_client.chat_completion(
                    messages=messages,
                    model=model,
                    system=system,
                    response_type=response_type,
                    stream=stream,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    prompt_template=prompt_template,
                    max_retries=max_retries-1,
                    **kwargs
                )
            self._handle_request_exception(None, False, e)
