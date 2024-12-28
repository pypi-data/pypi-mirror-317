from typing import List, Optional, Union, Generator
import requests
from requests.exceptions import RequestException

from .base import BaseClient
from pulsar.parser import parse
from pulsar.prompt import build_prompt, DEFAULT_PROMPT
import json

import logging
logger = logging.getLogger(__name__)


_allowed_roles = ("user", "assistant", "tool")


class OpenAiApiLikeException(Exception):
    """Custom exception for generic OpenAiApiLike errors"""
    pass


class OpenAiApiLike(BaseClient):
    """Base class implementing OpenAI-like API interface"""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _handle_request_exception(self, url: str, allow_one_retry: bool, e: RequestException):
        raise OpenAiApiLikeException(
            f"API request failed: {str(e)}\nURL: {url}\nResponse: {e.response.text if hasattr(e, 'response') else 'No response'}")

    def _make_request(self, endpoint: str, method: str = "POST", allow_one_retry=False, **kwargs):
        """Make HTTP request to the API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            self._handle_request_exception(
                url=url, allow_one_retry=allow_one_retry, e=e)
            self._make_request(
                endpoint=endpoint,
                method=method,
                allow_one_retry=False,
                **kwargs
            )

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
        """
        Generate chat completion using Groq's API

        Args:
            messages: List of Message objects containing the conversation
            model: The model ID
            system: Optional system message to set context
            response_type: Return type (str for content only, dict for full response)
            stream: Whether to stream the response
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            use_cot: Inject CoT prompt at end
            prompt_template: Use custom jinja2 prompt template
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated response as specified by response_type
        """
        for m in messages:
            if not m["role"] in _allowed_roles:
                raise ValueError(
                    f"role {m['role']}, should be one of {_allowed_roles}")

        if prompt_template is None:
            prompt_template = DEFAULT_PROMPT

        last_try = None
        tries = 0
        last_error = None
        while tries <= max_retries:
            build_messages = build_prompt(
                prompt_template=prompt_template,
                history=messages,
                system=system,
                response_type=response_type,
                last_try=last_try
            )
            payload = {
                "model": model,
                "messages": build_messages,
                "temperature": temperature,
                "stream": stream,
                **kwargs
            }

            if max_tokens:
                payload["max_tokens"] = max_tokens

            if stream:
                response = self.session.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    stream=True
                )
                return self._handle_stream(response, response_type)

            try:
                response = self._make_request(
                    "chat/completions", json=payload, allow_one_retry=True)
                last_try = response
                if response["choices"] is None:
                    raise ValueError("Got empty response from provider!")

                response_content = response["choices"][0]["message"]["content"]
                if response_type == str:
                    return response_content

                logger.debug(f"parsing: {response_content}")
                return parse(response_content, response_type)
            except Exception as e:
                tries += 1
                last_error = e
                pass

        if fallback_client is not None:
            return fallback_client.chat_completion(
                messages=messages,
                model=model,
                system=system,
                response_type=response_type,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                prompt_template=prompt_template,
                max_retries=max_retries,
                **kwargs
            )
        raise last_error

    def _handle_stream(self, response: requests.Response, response_type: type) -> Generator:
        """Handle streaming response from the API"""
        if response.status_code != 200:
            raise OpenAiApiLikeException(
                f"Stream request failed: {response.status_code}\nResponse: {response.text}")

        buffer = ""
        last_yield = None
        for line in response.iter_lines():
            if line:
                if line.startswith(b"data: "):
                    data = line[6:]  # Remove "data: " prefix
                    if data == b"[DONE]":
                        break
                    chunk = data.decode()
                    chunk_json = json.loads(chunk)
                    chunk_delta = chunk_json['choices'][0]['delta']
                    if 'content' in chunk_delta:
                        if response_type == str:
                            yield chunk_delta['content']
                        else:
                            buffer += chunk_delta['content']
                            try:
                                obj = parse(buffer, response_type,
                                            allow_partial=True)
                                if not isinstance(obj, str):
                                    if last_yield is None or str(last_yield) != str(obj):
                                        last_yield = str(obj)
                                        yield obj
                            except:
                                pass
