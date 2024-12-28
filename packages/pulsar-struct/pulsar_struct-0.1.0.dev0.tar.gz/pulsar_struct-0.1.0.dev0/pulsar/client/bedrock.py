from typing import List, Optional, Union, Generator, Callable
import json
import boto3

from pulsar.parser import parse
from pulsar.prompt import build_prompt, DEFAULT_PROMPT

from .base import BaseClient


class BedrockException(Exception):
    """Custom exception for Bedrock API errors"""
    pass


class BedrockClient(BaseClient):
    """Client for interacting with AWS Bedrock"""

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: str = "us-east-1"
    ):
        super().__init__(None, None)

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.client = session.client('bedrock-runtime')

    def _handle_request_exception(self, url: str, allow_one_retry: bool, e: Exception):
        raise BedrockException(f"Bedrock API request failed: {str(e)}")

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
            # Format messages based on model provider
            if "anthropic" in model:
                # Format for Claude models
                formatted_messages = []
                if system:
                    formatted_messages.append(
                        {"role": "system", "content": system})
                formatted_messages.extend([
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in messages
                ])

                payload = {
                    "messages": formatted_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens if max_tokens else 2048,
                    **kwargs
                }
            else:
                # Format for other models (e.g., Titan)
                prompt = ""
                if system:
                    prompt += f"System: {system}\n"
                for msg in messages:
                    prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"

                payload = {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "temperature": temperature,
                        "maxTokens": max_tokens if max_tokens else 2048,
                        **kwargs
                    }
                }

            if stream:
                response = self.client.invoke_model_with_response_stream(
                    modelId=model,
                    body=json.dumps(payload)
                )
                return self._handle_bedrock_stream(response, response_type)
            else:
                response = self.client.invoke_model(
                    modelId=model,
                    body=json.dumps(payload)
                )
                response_body = json.loads(response['body'].read())

                if "anthropic" in model:
                    response_content = response_body['content'][0]['text']
                else:
                    response_content = response_body['results'][0]['outputText']

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

    def _handle_bedrock_stream(self, response: dict, response_type: type) -> Generator:
        """Handle streaming response from Bedrock"""
        for event in response['body']:
            chunk = json.loads(event['chunk']['bytes'])
            if "anthropic" in response['modelId']:
                if 'content' in chunk and chunk['content']:
                    yield chunk['content'][0]['text']
            else:
                if 'outputText' in chunk:
                    yield chunk['outputText']
