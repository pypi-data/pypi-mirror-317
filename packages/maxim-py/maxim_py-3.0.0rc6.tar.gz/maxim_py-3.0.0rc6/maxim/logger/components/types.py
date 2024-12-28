import json
from dataclasses import asdict, dataclass
from datetime import date, datetime
from enum import Enum
from types import SimpleNamespace
from typing import Any, Dict, Optional


class Entity(Enum):
    SESSION = "session"
    TRACE = "trace"
    SPAN = "span"
    TOOL_CALL = "tool_call"
    GENERATION = "generation"
    FEEDBACK = "feedback"
    RETRIEVAL = "retrieval"


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class CommitLog:
    def __init__(self, entity: Entity, entity_id: str, action: str, data: Optional[Dict[str, Any]] = None):
        self.entity = entity
        self.entity_id = entity_id
        self.action = action
        self.data = data

    def serialize(self, custom_data: Optional[Dict[str,Any]] = None) -> str:
        if custom_data is not None:
            if self.data is None:
                self.data = {}
            self.data.update(custom_data)
        return f"{self.entity.value}{{id={self.entity_id},action={self.action},data={json.dumps(self.data,cls=DateTimeEncoder)}}}"


def object_to_dict(obj):
    if isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [object_to_dict(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif hasattr(obj, "__dict__"):
        return object_to_dict(obj.__dict__)
    elif isinstance(obj, SimpleNamespace):
        return object_to_dict(vars(obj))
    else:
        return str(obj)

@dataclass
class GenerationError:
    message: str
    code: Optional[str] = None
    type: Optional[str] = None
