import logging
import sys
from bdb import GENERATOR_AND_COROUTINE_FLAGS
from configparser import LegacyInterpolation
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID, uuid4

import maxim

# Use LangChain features
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.outputs import LLMResult
from maxim import expiringKeyValueStore
from maxim.logger.langchain.utils import parse_base_message_to_maxim_generation

from ...expiringKeyValueStore import ExpiringKeyValueStore
from ...logger import (
    GenerationConfig,
    Logger,
    RetrievalConfig,
    Span,
    SpanConfig,
    ToolCall,
    ToolCallConfig,
    TraceConfig,
)
from .utils import (parse_langchain_llm_error, parse_langchain_llm_result,
                    parse_langchain_messages,
                    parse_langchain_model_and_provider,
                    parse_langchain_model_parameters, parse_langchain_provider)

logger = logging.getLogger("MaximSDK")


# 20 minutes
DEFAULT_TIMEOUT = 60 * 20


class ChainType(Enum):
    CHAIN = "chain"
    GENERATION = "generation"
    TOOL = "tool"


class MaximLangchainTracer(BaseCallbackHandler):
    """A callback handler that logs langchain outputs to Maxim logger

    Args:
        logger: Logger: Maxim Logger instance to log outputs
    """

    def __init__(self, logger: Logger, metadata: Optional[Dict[str, Any]]) -> None:
        """Initializes the Langchain Tracer
        Args:
            logger: Logger: Maxim Logger instance to log outputs
        """
        super().__init__()
        self.logger = logger
        self.chains = ExpiringKeyValueStore()
        self.containers = ExpiringKeyValueStore()
        self.tool_calls = ExpiringKeyValueStore()
        self.generations = ExpiringKeyValueStore()
        self.retrievals = ExpiringKeyValueStore()
        self.metadata_store = ExpiringKeyValueStore()
        self.metadata = None
        if metadata is not None:
            self._validate_maxim_metadata(metadata)
            self.metadata = metadata

    def _get_chain_type(self, messages: List[Any]) -> ChainType:
        # Checking if there is already a generation running for this run_id
        if len(messages) == 0:
            return ChainType.CHAIN
        # Now we will check if the messages are type of one of the messages
        try:
            if any(isinstance(message, FunctionMessage) for message in messages) or any(
                isinstance(message, ToolMessage) for message in messages
            ):
                return ChainType.TOOL
            if any(
                isinstance(
                    message, (HumanMessage, AIMessage, ChatMessage, SystemMessage)
                )
                for message in messages
            ):
                return ChainType.GENERATION

            return ChainType.CHAIN
        except Exception as e:
            return ChainType.CHAIN

    def _validate_maxim_metadata(self, metadata: Dict[str, Any]):
        if metadata is None:
            return
        id_keys = ["session_id", "trace_id", "span_id"]
        present_keys = [key for key in id_keys if key in metadata]
        if len(present_keys) > 1:
            raise ValueError(
                f"Multiple keys found in metadata: {present_keys}. You can pass only one of these."
            )
        valid_keys = [
            "session_id",
            "trace_id",
            "span_id",
            "generation_tags",
            "retrieval_tags",
            "trace_tags",
            "retrieval_name",
            "trace_name",
            "generation_name",
        ]
        invalid_keys = [key for key in metadata if key not in valid_keys]
        if len(invalid_keys) > 0:
            raise ValueError(
                f"Invalid keys found in metadata: {invalid_keys}. Valid keys are {valid_keys}"
            )

    def _get_container(self, run_id: UUID):
        # Now we will checking in containers
        if self.containers.get(str(run_id)) is not None:
            container = self.containers.get(str(run_id))
            if container.startswith("span:"):
                return container.split(":", 1)
            if container.startswith("trace:"):
                return container.split(":", 1)
            if container.startswith("session:"):
                return container.split(":", 1)
            return None, None
        return None, None

    def _get_container_from_metadata(self, run_id: UUID):
        maxim_metadata = self.metadata_store.get(str(run_id))
        if maxim_metadata is not None:
            span_id = maxim_metadata.get("span_id", None)
            if span_id is not None:
                return "span", span_id
            session_id = maxim_metadata.get("session_id", None)
            if session_id is not None:
                return "session", session_id
            trace_id = maxim_metadata.get("trace_id", None)
            if trace_id is not None:
                return "trace", trace_id
        return "local_trace", str(run_id)

    # LLM callbacks

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[MaximSDK: Langchain] on_llm_start called")
        model, model_parameters = parse_langchain_model_parameters(**kwargs)
        provider = parse_langchain_provider(serialized)
        model, provider = parse_langchain_model_and_provider(model, provider)
        messages = parse_langchain_messages(prompts)
        generation_id = str(uuid4())
        generation_name = None
        generation_tags = None
        trace_tags = None

        if metadata is not None and metadata.get("maxim", None) is not None:
            self._validate_maxim_metadata(metadata.get("maxim", None))
            self.metadata_store.set(
                str(run_id), metadata.get("maxim", None), DEFAULT_TIMEOUT
            )
            trace_tags = metadata.get("maxim", {}).get("trace_tags", None)
            generation_name = metadata.get("maxim", {}).get("generation_name", None)
            generation_tags = metadata.get("maxim", {}).get("generation_tags", None)
        elif self.metadata is not None:
            self.metadata_store.set(str(run_id), self.metadata, DEFAULT_TIMEOUT)
            trace_name = self.metadata.get("trace_name", None)
            trace_tags = self.metadata.get("trace_tags", None)
            generation_name = self.metadata.get("generation_name", None)
            generation_tags = self.metadata.get("generation_tags", None)

        generation_config = GenerationConfig(
            id=generation_id,
            name=generation_name,
            provider=provider,
            model=model,
            messages=messages,
            model_parameters=model_parameters,
            tags=generation_tags,
        )

        self.generations.set(str(run_id), generation_id, DEFAULT_TIMEOUT)

        container, container_id = self._get_container_from_metadata(run_id)

        if container == "span":
            self.logger.span_generation(container_id, generation_config)
        elif container == "trace":
            self.logger.trace_generation(container_id, generation_config)
        elif container == "session":
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.session_trace(
                container_id,
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags),
            )
            trace.generation(generation_config)
        else:
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.trace(
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags)
            )
            trace.generation(generation_config)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        logger.debug(f"[MaximSDK: Langchain] on_llm_end called")
        run_id = kwargs.get("run_id", None)
        if run_id is not None:
            result = parse_langchain_llm_result(response)
            generation_id = self.generations.get(str(run_id))
            if generation_id is not None:
                container, container_id = self._get_container_from_metadata(run_id)
                self.logger.generation_result(generation_id, result)
                if container == "local_trace":
                    self.logger.trace_end(container_id)

    # Retrieval callbacks

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[Langchain] on_retriever_start called")
        """Run when Retriever starts running."""
        container, container_id = self._get_container_from_metadata(run_id)
        retrieval_id = str(uuid4())
        retrieval_config = RetrievalConfig(id=retrieval_id)
        if container == "span":
            retrieval = self.logger.span_retrieval(
                container_id, config=retrieval_config
            )
            retrieval.input(query)
        elif container == "trace":
            retrieval = self.logger.trace_retrieval(
                container_id, config=retrieval_config
            )
            retrieval.input(query)
        elif container == "session":
            trace = self.logger.session_trace(container_id, TraceConfig(id=str(run_id)))
            retrieval = trace.retrieval(retrieval_config)
            retrieval.input(query)
        else:
            retrieval = self.logger.trace_retrieval(
                str(run_id), config=retrieval_config
            )
            retrieval.input(query)

    def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[Langchain] on_retriever_end called")
        trace_id = str(run_id)
        retrieval_id = self.retrievals.get(trace_id)
        if retrieval_id is not None:
            self.logger.retrieval_output(retrieval_id, documents)

    # ChatModel callbacks

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[Langchain] on_chat_model_start called")
        run_id = kwargs.get("run_id", None)
        model, model_parameters = parse_langchain_model_parameters(**kwargs)
        provider = parse_langchain_provider(serialized)
        model, provider = parse_langchain_model_and_provider(model, provider)
        maxim_messages = parse_langchain_messages(messages)
        generation_id = str(uuid4())
        # Checking if generation id already present for this run_id
        if self.generations.get(str(run_id)) is not None:
            generation_id = self.generations.get(str(run_id))
        generation_name = None
        generation_tags = None
        trace_tags = None
        trace_name = None

        if metadata is not None and metadata.get("maxim", None) is not None:
            self._validate_maxim_metadata(metadata.get("maxim", None))
            self.metadata_store.set(
                str(run_id), metadata.get("maxim", None), DEFAULT_TIMEOUT
            )
            trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace_tags = metadata.get("maxim", {}).get("trace_tags", None)
            generation_name = metadata.get("maxim", {}).get("generation_name", None)
            generation_tags = metadata.get("maxim", {}).get("generation_tags", None)
        elif self.metadata is not None:
            self.metadata_store.set(str(run_id), self.metadata, DEFAULT_TIMEOUT)
            trace_name = self.metadata.get("trace_name", None)
            trace_tags = self.metadata.get("trace_tags", None)
            generation_name = self.metadata.get("generation_name", None)
            generation_tags = self.metadata.get("generation_tags", None)

        generation_config = GenerationConfig(
            id=generation_id,
            name=generation_name,
            provider=provider,
            model=model,
            messages=maxim_messages,
            model_parameters=model_parameters,
            tags=generation_tags,
        )
        self.generations.set(str(run_id), generation_id, DEFAULT_TIMEOUT)

        container, container_id = self._get_container_from_metadata(run_id)

        if container == "span":
            self.logger.span_generation(container_id, generation_config)
        elif container == "trace":
            self.logger.trace_generation(container_id, generation_config)
        elif container == "session":
            trace = self.logger.session_trace(
                container_id,
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags),
            )
            trace.generation(generation_config)
        else:
            trace = self.logger.trace(
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags)
            )
            trace.generation(generation_config)

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        logger.debug(f"[Langchain] on_llm_error called")
        run_id = kwargs.get("run_id", None)
        if run_id is not None:
            generation_id = self.generations.get(str(run_id))
            if generation_id is not None:
                container, container_id = self._get_container_from_metadata(run_id)
                generation_error = parse_langchain_llm_error(error)
                self.logger.generation_error(generation_id, generation_error)
                if container == "local_trace":
                    self.logger.trace_end(container_id)

    # Chain callbacks

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        try:
            # We hide the hidden chains
            if "langsmith:hidden" in kwargs.get("tags", []):
                return
            parent_run_id = kwargs.get("parent_run_id", None)
            run_id = kwargs.get("run_id", None)
            span_name = kwargs.get("name", None)
            span: Optional[Span] = None
            span_id = str(uuid4())
            tags: Dict[str, str] = {}
            tags["run_id"] = str(run_id)
            if parent_run_id is not None:
                tags["parent_run_id"] = str(parent_run_id)
            if kwargs.get("tags", None) is not None:
                for tag in kwargs["tags"]:
                    key, value = tag.split(":", 1)
                    tags[key.strip()] = value.strip()
            metadata = kwargs.get("metadata", None)
            if metadata is not None:
                for key, value in kwargs["metadata"].items():
                    tags[key.strip()] = str(value)

            # Checking if this is a generation
            messages = inputs["messages"] if "messages" in inputs else []
            chain_type = self._get_chain_type(messages=messages)

            if chain_type == ChainType.TOOL:
                container, container_id = self._get_container(str(parent_run_id))
                if container is not None:
                    self.containers.set(
                        str(run_id),
                        f"{container}:{container_id}",
                        DEFAULT_TIMEOUT,
                    )

            if chain_type == ChainType.GENERATION:
                # Here we just create generation id and push it against the run_id
                # This we do to avoid any duplicate generations getting created
                # if users end up adding decorators or tracing the individual model calls

                # Checking if generation exists
                if self.generations.get(str(parent_run_id)) is not None:
                    # This means that the first message of the inputs is going to be AIMessage
                    # We will update this generation and end it
                    message = messages[-1]
                    generation_id = self.generations.get(str(parent_run_id))
                    if isinstance(message, AIMessage):
                        # Updating the generation
                        model = message.response_metadata.get("model", "unknown")
                        self.logger.generation_set_model(generation_id, model)
                        self.logger.generation_result(
                            generation_id=generation_id, result=message
                        )
                    return

                # This means that this is a new turn
                # We will check if the last message is AIMessage
                # If its AIMessage - then its most likely a tool call
                # Else we will pick the last HumanMessage and create a new generation
                if isinstance(messages[-1], AIMessage):
                    # This means its the next round
                    # Here checking if there is a tool_call
                    # If yes, updating chain
                    message = messages[-1]
                    tool_calls = message.tool_calls or []
                    if len(tool_calls) > 0:
                        container, container_id = self._get_container(
                            str(parent_run_id)
                        )
                        if container is not None:
                            self.containers.set(
                                str(run_id),
                                f"{container}:{container_id}",
                                DEFAULT_TIMEOUT,
                            )
                    # Rest of the flow will be handled in the tool_call_start and tool_call_end
                    return
                elif isinstance(messages[-1], ToolMessage):
                    # We attach the container again to send the events
                    container, container_id = self._get_container(str(parent_run_id))
                    if container is not None:
                        self.containers.set(
                            str(run_id),
                            f"{container}:{container_id}",
                            DEFAULT_TIMEOUT,
                        )
                else:
                    # We will only keep last message in messages
                    messages = [messages[-1]]

                span_id = self.chains.get(str(parent_run_id))
                # Creating a new generation
                generation_id = str(uuid4())
                # Creating the generation
                # This is a placeholder generation
                # Rest of the information will be added when chain ends
                parsed_messages = parse_langchain_messages([messages])
                self.logger.span_add_generation(
                    span_id,
                    GenerationConfig(
                        id=generation_id,
                        name=span_name,
                        # openai is the default provider we use for now
                        provider="unknown",
                        model="unknown",
                        messages=parsed_messages,
                        tags=tags,
                    ),
                )
                self.containers.set(str(run_id), f"span:{span_id}", DEFAULT_TIMEOUT)
                self.generations.set(str(run_id), generation_id, DEFAULT_TIMEOUT)
                return

            if chain_type == ChainType.CHAIN:
                # It's a span, so create one and move on
                if parent_run_id is None:
                    span_config = SpanConfig(id=span_id, name=span_name, tags=tags)
                    # this is the core id so add it to the span
                    self.chains.set(str(run_id), span_id, DEFAULT_TIMEOUT)
                    container, container_id = self._get_container_from_metadata(run_id)
                    event_id = str(uuid4())
                    if container == "span":
                        span = self.logger.span_add_sub_span(container_id, span_config)
                        self.logger.span_event(span.id, event_id, "start", tags)
                    elif container == "trace":
                        span = self.logger.trace_add_span(container_id, span_config)
                        self.logger.span_event(span.id, event_id, "start", tags)
                    else:
                        # Checking if I have current trace
                        if self.metadata is not None:
                            trace_id = self.metadata["trace_id"]
                            if trace_id is not None:
                                span = self.logger.trace_add_span(trace_id, span_config)
                                self.logger.span_event(span.id, event_id, "start", tags)
                        else:
                            # Creating trace locally
                            trace_name = None
                            trace = self.logger.trace(
                                TraceConfig(id=str(run_id), name=trace_name)
                            )
                            span = trace.span(span_config)
                            self.logger.span_event(span.id, event_id, "start", tags)
                else:
                    span_id = self.chains.get(str(parent_run_id))
                    new_span_id = str(uuid4())
                    span_config = SpanConfig(id=new_span_id, name=span_name, tags=tags)
                    self.chains.set(str(run_id), new_span_id, DEFAULT_TIMEOUT)
                    span = self.logger.span_add_sub_span(span_id, span_config)

                if span is not None:
                    # Getting existing metadata
                    new_meta = {"span_id": span.id}
                    run_meta = self.metadata_store.get(str(run_id))
                    if run_meta is not None:
                        new_meta.update(run_meta)
                    # Here we will set the container for the given run_id
                    self.containers.set(str(run_id), f"span:{span.id}", DEFAULT_TIMEOUT)
                    self.metadata_store.set(str(run_id), new_meta, DEFAULT_TIMEOUT)

                span_id = self.chains.get(str(parent_run_id))
                if span_id is None:
                    logger.error("[MaximSDK] No span id found for chain")
                    return
                tool_message: ToolMessage = next(
                    (
                        message
                        for message in reversed(messages)
                        if isinstance(message, ToolMessage)
                    ),
                    None,
                )
                if tool_message is None:
                    return
                # Find the AI message in messages
                # Which has the tool call
                args = ""
                for message in messages:
                    if isinstance(message, AIMessage):
                        tool_calls = message.tool_calls or []
                        for tool_call in tool_calls:
                            if tool_call["id"] == tool_message.tool_call_id:
                                args = tool_call["args"]
                                break
                tool_call_id = str(uuid4())
                tool_call = self.logger.span_tool_call(
                    span_id,
                    ToolCallConfig(
                        id=tool_call_id, name=tool_message.name, args=args, tags=tags
                    ),
                )
                print("tool start")
                return
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse chain-start: {e}")

    def on_chain_end(self, outputs: Union[str, Dict[str, Any]], **kwargs: Any) -> Any:
        try:
            # We hide the hidden chains
            if "langsmith:hidden" in kwargs.get("tags", []):
                return
            run_id = kwargs.get("run_id", None)
            parent_run_id = kwargs.get("parent_run_id", None)
            tags = {
                tag.split(":")[0]: tag.split(":")[1]
                for tag in kwargs.get("tags", [])
                if ":" in tag
            }
            # Getting chain type
            chain_type = self._get_chain_type(
                messages=(
                    outputs["messages"] if isinstance(outputs, dict) else [outputs]
                ),
            )
            if chain_type == ChainType.CHAIN or chain_type == ChainType.TOOL:
                if isinstance(outputs, str):
                    # we fire this as event
                    if parent_run_id is not None:
                        container, container_id = self._get_container(parent_run_id)
                        event_id = str(uuid4())
                        if container == "span":
                            self.logger.span_event(
                                container_id, event_id, outputs, tags
                            )
                        elif container == "trace":
                            self.logger.trace_event(
                                container_id, event_id, outputs, tags
                            )
                if run_id is not None:
                    span_id = self.chains.get(str(run_id))
                    if span_id is not None:
                        self.logger.span_end(span_id)
                    self.chains.delete(str(run_id))
                    self.metadata_store.delete(str(run_id))

            if chain_type == ChainType.GENERATION:
                self.generations.delete(str(run_id))

            self.containers.delete(str(run_id))
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse chain-end: {e}")

    def on_chain_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        print("chain-error", error, kwargs)

    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        print("on-agent-action", action, run_id, parent_run_id, kwargs)

    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        print("on-agent-finish", finish, run_id, parent_run_id, kwargs)

    # Tool callbacks

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        try:
            run_id = kwargs.get("run_id", None)
            parent_run_id = kwargs.get("parent_run_id", None)
            name = serialized.get("name", None)
            description = serialized.get("description", None)
            container, container_id = self._get_container(str(parent_run_id))
            if container is None:
                container, container_id = self._get_container_from_metadata(
                    parent_run_id
                )
            if container == "span":
                tool_call = self.logger.span_add_tool_call(
                    container_id,
                    ToolCallConfig(
                        id=str(uuid4()),
                        name=name,
                        description=description,
                        args=input_str,
                    ),
                )
                self.tool_calls.set(str(run_id), tool_call.id, DEFAULT_TIMEOUT)
            elif container == "trace":
                tool_call = self.logger.trace_add_tool_call(
                    container_id,
                    ToolCallConfig(
                        id=str(uuid4()),
                        name=name,
                        description=description,
                        args=input_str,
                    ),
                )
                self.tool_calls.set(str(run_id), tool_call.id, DEFAULT_TIMEOUT)
            else:
                logger.error(
                    "[MaximSDK] No container found for tool call. This is invalid state."
                )
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse tool-start: {e}")

    def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
        try:
            run_id = kwargs.get("run_id", None)
            tool_call_id = self.tool_calls.get(str(run_id))
            if tool_call_id is None:
                logger.error(
                    "[MaximSDK] No tool call id found for tool end. This is invalid state."
                )
                return
            if isinstance(output, ToolMessage):
                if output.status == "success":
                    self.logger.tool_call_result(tool_call_id, output.content)
                elif output.status == "error":
                    self.logger.tool_call_error(tool_call_id, output.content)
            else:
                logger.error(
                    f"[MaximSDK] Invalid output type {type(output)}. This is invalid state."
                )
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse tool-end: {e}")

    def on_tool_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        try:
            run_id = kwargs.get("run_id", None)
            tool_call_id = self.tool_calls.get(str(run_id))
            if tool_call_id is None:
                logger.error(
                    "[MaximSDK] No tool call id found for tool end. This is invalid state."
                )
                return
            self.logger.tool_call_error(tool_call_id, str(error))
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse tool-end: {e}")

    def on_text(self, text: str, **kwargs: Any) -> Any:
        print("on-text", text, kwargs)
