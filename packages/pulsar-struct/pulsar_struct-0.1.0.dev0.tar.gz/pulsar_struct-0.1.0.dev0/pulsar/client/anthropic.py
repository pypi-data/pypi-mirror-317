from typing import List, Optional, Union, Generator
from anthropic import Anthropic

from pulsar.parser import parse
from pulsar.prompt import build_prompt, DEFAULT_PROMPT

from .base import BaseClient


class AnthropicException(Exception):
    """Custom exception for Anthropic API errors"""
    pass


class AnthropicClient(BaseClient):
    """Client for interacting with Anthropic's Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            import os
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided or set as ANTHROPIC_API_KEY environment variable")

        super().__init__(api_key, None)
        self.client = Anthropic(api_key=api_key)

    def _handle_request_exception(self, url: str, allow_one_retry: bool, e: Exception):
        raise AnthropicException(f"Anthropic API request failed: {str(e)}")

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
            # Convert messages to Anthropic format
            formatted_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    formatted_messages.append(
                        {"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    formatted_messages.append(
                        {"role": "assistant", "content": msg["content"]})

            message = self.client.messages.create(
                model=model,
                messages=formatted_messages,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                **kwargs
            )

            if stream:
                def stream_generator():
                    for chunk in message:
                        if chunk.content:
                            yield chunk.content[0].text
                return stream_generator()

            response_content = message.content[0].text
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
