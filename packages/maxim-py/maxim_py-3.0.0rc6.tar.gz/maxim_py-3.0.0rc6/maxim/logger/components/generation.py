import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from ..parsers.generation_parser import parse_model_parameters, parse_result
from ..writer import LogWriter
from .base import BaseContainer
from .types import Entity, GenerationError, object_to_dict

logger = logging.getLogger("MaximSDK")


@dataclass
class GenerationConfig:
    id: str
    provider: str
    model: str
    messages: Optional[List[Any]] = field(default_factory=list)
    model_parameters: Dict[str, Any] = field(default_factory=dict)
    span_id: Optional[str] = None
    name: Optional[str] = None
    maxim_prompt_id: Optional[str] = None
    tags: Optional[Dict[str, str]] = None


valid_providers = [
    "openai",
    "azure",
    "anthropic",
    "huggingface",
    "together",
    "google",
    "groq",
    "bedrock",
    "cohere",
    "unknown",
]


class Generation(BaseContainer):
    def __init__(self, config: GenerationConfig, writer: LogWriter):
        super().__init__(Entity.GENERATION, config.__dict__, writer)
        self.model = config.model
        self.maxim_prompt_id = config.maxim_prompt_id
        self.messages = []
        self.provider = config.provider
        self.provider = config.provider.lower()
        if self.provider not in valid_providers:
            self.provider = "unknown"
        if config.messages is not None:
            self.messages.extend(config.messages)
        self.model_parameters = parse_model_parameters(config.model_parameters)

    def _set_provider(self, writer: LogWriter, id: str, provider: str):
        if provider not in valid_providers:
            raise ValueError(
                f"Invalid provider: {self.provider}. Must be one of {', '.join(valid_providers)}."
            )
        BaseContainer._commit_(
            writer, Entity.GENERATION, id, "update", {"provider": provider}
        )

    def set_provider(self, provider: str):
        if provider not in valid_providers:
            raise ValueError(
                f"Invalid provider: {self.provider}. Must be one of {', '.join(valid_providers)}."
            )
        self.provider = provider

    @staticmethod
    def set_model_(writer: LogWriter, id: str, model: str):
        BaseContainer._commit_(
            writer, Entity.GENERATION, id, "update", {"model": model}
        )

    def set_model(self, model: str):
        self.model = model
        self._commit("update", {"model": model})

    @staticmethod
    def add_message_(writer: LogWriter, id: str, message: Any):
        BaseContainer._commit_(
            writer, Entity.GENERATION, id, "update", {"messages": [message]}
        )

    def add_message(self, message: Any):
        self.messages.append(message)
        self._commit("update", {"messages": [message]})

    @staticmethod
    def set_model_parameters_(
        writer: LogWriter, id: str, model_parameters: Dict[str, Any]
    ):
        BaseContainer._commit_(
            writer,
            Entity.GENERATION,
            id,
            "update",
            {"model_parameters": model_parameters},
        )

    def set_model_parameters(self, model_parameters: Dict[str, Any]):
        self.model_parameters = model_parameters
        self._commit("update", {"model_parameters": model_parameters})

    @staticmethod
    def result_(writer: LogWriter, id: str, result: Any):
        try:
            # Checking the type
            result = Generation.convert_result(result)
            # Validating the result
            parse_result(result)
            BaseContainer._commit_(
                writer, Entity.GENERATION, id, "result", {"result": result}
            )
            BaseContainer._end_(
                writer,
                Entity.GENERATION,
                id,
                {
                    "endTimestamp": datetime.now(timezone.utc),
                },
            )
        except ValueError as e:
            logger.error(
                "Invalid result. You can pass OpenAI/Azure ChatCompletion or Langchain LLMResult,AIMessage: {e}"
            )
            raise ValueError(
                f"Invalid result. You can pass OpenAI/Azure ChatCompletion or Langchain LLMResult,AIMessage: {e}"
            )

    @staticmethod
    def end_(writer: LogWriter, id: str, data: Optional[Dict[str, Any]] = None):
        if data is None:
            data = {}
        BaseContainer._end_(
            writer,
            Entity.GENERATION,
            id,
            {
                "endTimestamp": datetime.now(timezone.utc),
                **data,
            },
        )

    @staticmethod
    def add_tag_(writer: LogWriter, id: str, key: str, value: str):
        BaseContainer._add_tag_(writer, Entity.GENERATION, id, key, value)

    @staticmethod
    def convert_chat_completion(chat_completion: dict):
        return {
            "id": chat_completion.get("id", str(uuid4())),
            "created": chat_completion.get("created", datetime.now(timezone.utc)),
            "choices": [
                {
                    "index": choice.get("index", 0),
                    "message": {
                        "role": choice.get("message").get("role", "assistant"),
                        "content": choice.get("message").get("content", ""),
                        "tool_calls": choice.get("message").get("tool_calls", None),
                        "function_calls": choice.get("message").get(
                            "function_calls", None
                        ),
                    },
                    "finish_reason": choice.get("finish_reason", None),
                    "logprobs": choice.get("logprobs", None),
                }
                for choice in chat_completion.get("choices", [])
            ],
            "usage": chat_completion.get("usage", {}),
        }

    @staticmethod
    def convert_result(result: Any):
        try:
            parse_result(result)
            return result
        except Exception as err:
            result_dict = object_to_dict(result)
            if isinstance(result_dict, dict):
                # Checking if its Azure or OpenAI result
                if (
                    "object" in result_dict
                    and result_dict["object"] == "chat.completion"
                ):
                    return Generation.convert_chat_completion(result_dict)
                elif (
                    "object" in result_dict
                    and result_dict["object"] == "text.completion"
                ):
                    raise ValueError("Text completion is not yet supported.")
                elif isinstance(result, object):
                    try:
                        from langchain_core.messages import AIMessage
                        from langchain_core.outputs import LLMResult

                        from ..langchain.utils import (
                            parse_base_message_to_maxim_generation,
                            parse_langchain_llm_result)
                        if isinstance(result, AIMessage):
                            return parse_base_message_to_maxim_generation(result)
                        elif isinstance(result, LLMResult):
                            return parse_langchain_llm_result(result)
                    except ImportError:
                        pass
            return result

    def result(self, result: Any):
        try:
            # Checking the type
            result = Generation.convert_result(result)
            # Validating the result
            parse_result(result)
            # Logging the result
            self._commit("result", {"result": result})
            self.end()
        except ValueError as e:
            logger.error(
                f"Invalid result. You can pass OpenAI/Azure ChatCompletion or Langchain LLMResult,AIMessage: {e}"
            )
            raise ValueError(
                f"Invalid result. You can pass OpenAI/Azure ChatCompletion or Langchain LLMResult,AIMessage: {e}"
            )

    def error(self, error: GenerationError):
        if not error.code:
            error.code = ""
        if not error.type:
            error.type = ""
        self._commit(
            "result",
            {
                "result": {
                    "error": {
                        "message": error.message,
                        "code": error.code,
                        "type": error.type,
                    },
                    "id": str(uuid4()),
                }
            },
        )
        self.end()

    @staticmethod
    def error_(writer: LogWriter, id: str, error: GenerationError):
        if not error.code:
            error.code = ""
        if not error.type:
            error.type = ""
        BaseContainer._commit_(
            writer,
            Entity.GENERATION,
            id,
            "result",
            {
                "result": {
                    "error": {
                        "message": error.message,
                        "code": error.code,
                        "type": error.type,
                    },
                    "id": str(uuid4()),
                }
            },
        )
        BaseContainer._end_(
            writer,
            Entity.GENERATION,
            id,
            {
                "endTimestamp": datetime.now(timezone.utc),
            },
        )

    def data(self) -> Dict[str, Any]:
        base_data = super().data()
        return {
            **base_data,
            "model": self.model,
            "provider": self.provider,
            "maximPromptId": self.maxim_prompt_id,
            "messages": self.messages,
            "modelParameters": self.model_parameters,
        }
