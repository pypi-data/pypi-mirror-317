from typing import Union, Optional, List, Generator

from .anthropic import AnthropicClient
from .base import BaseClient
from .bedrock import BedrockClient
from .gemini import GeminiClient
from .groq import GroqClient
from .ollama import OllamaClient
from .openai_like import OpenAiApiLike
from .openai import OpenAIClient
from .openrouter import OpenRouterClient


provide_map = {
    "groq": GroqClient,
    "openrouter": OpenRouterClient,
    "ollama": OllamaClient,
    "anthropic": AnthropicClient,
    "gemini": GeminiClient,
    "bedrock": BedrockClient
}


class Client:
    @staticmethod
    def from_provider(provider: str, **kwargs):
        return provide_map[provider](**kwargs)

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
        provider, model_name = model.split("/")
        client = Client.from_provider(provider)
        return client.chat_completion(
            messages=messages,
            model=model_name,
            system=system,
            response_type=response_type,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            prompt_template=prompt_template,
            max_retries=max_retries,
            fallback_client=fallback_client,
            **kwargs
        )


__all__ = ["AnthropicClient", "BaseClient", "BedrockClient", "GeminiClient", "GroqClient",
           "OllamaClient", "OpenAiApiLike", "OpenAIClient", "OpenRouterClient", "Client"]
