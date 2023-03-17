from dataclasses import dataclass, InitVar, field
from typing import List, Dict

import openai
from openai.openai_object import OpenAIObject


@dataclass
class OpenAIChatCompletionAPIRequest:
    messages: List[Dict[str, str]]
    api_key: str = "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"
    model: str = "gpt-3.5-turbo"


@dataclass
class OpenAIChatCompletionAPIResult:
    raw_api_response: InitVar[OpenAIObject]
    messages: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self, raw_api_response):
        for choice in raw_api_response["choices"]:
            self.messages.append(choice["message"])


class OpenAIChatCompletionAPI:

    def __init__(self):
        self.chat_completion = openai.ChatCompletion()

    def create(self, request: OpenAIChatCompletionAPIRequest) -> OpenAIChatCompletionAPIResult:
        raw_api_response = self.chat_completion.create(
            api_key=request.api_key,
            model=request.model,
            messages=request.messages,
        )
        return OpenAIChatCompletionAPIResult(raw_api_response)
