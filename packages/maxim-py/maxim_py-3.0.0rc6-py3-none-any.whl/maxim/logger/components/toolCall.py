import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ..writer import LogWriter
from .base import BaseContainer
from .types import Entity

logger = logging.getLogger("MaximSDK")


@dataclass
class ToolCallConfig:
    id: str
    name: str
    description: str
    args: str
    tags: Optional[Dict[str, str]] = None


@dataclass
class ToolCallError:
    message: str
    code: Optional[str] = None
    type: Optional[str] = None


class ToolCall(BaseContainer):
    def __init__(self, config: ToolCallConfig, writer: LogWriter):
        super().__init__(Entity.TOOL_CALL, config.__dict__, writer)
        self._id = config.id
        self._name = config.name
        self.args = config.args
        self.description = config.description
        self.tags = config.tags

    @staticmethod
    def result_(writer: LogWriter, id: str, result: str):
        BaseContainer._commit_(
            writer, Entity.TOOL_CALL, id, "result", {"result": result}
        )
        BaseContainer._end_(
            writer,
            Entity.TOOL_CALL,
            id,
            {
                "endTimestamp": datetime.now(timezone.utc),
            },
        )

    def result(self, result: str):
        self._commit("result", {"result": result})
        self.end()

    def error(self, error: ToolCallError):
        self._commit("error", {"error": error})
        self.end()

    @staticmethod
    def error_(writer: LogWriter, id: str, error: ToolCallError):
        BaseContainer._commit_(writer, Entity.TOOL_CALL, id, "error", {"error": error})
        BaseContainer._end_(
            writer,
            Entity.TOOL_CALL,
            id,
            {
                "endTimestamp": datetime.now(timezone.utc),
            },
        )

    def data(self) -> Dict[str, Any]:
        base_data = super().data()
        return {
            **base_data,
            "name": self._name,
            "description": self.description,
            "args": self.args,
        }
