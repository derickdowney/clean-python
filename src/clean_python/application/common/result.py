from dataclasses import dataclass
from enum import Enum
from typing import Any


class ErrorCode(Enum):
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"


@dataclass(frozen=True)
class Error:
    """Standarized error information"""

    code: ErrorCode
    message: str
    details: dict[str, Any] | None = None

    @classmethod
    def not_found(cls, entity: str, entity_id: str) -> Error:
        return cls(
            code=ErrorCode.NOT_FOUND, message=f"{entity} with id {entity_id} not found"
        )


@dataclass(frozen=True)
class Result:
    """Represents success or failure of a use case execution"""

    value: Any = None
    error: Error | None = None

    @classmethod
    def failure(cls, error: Error) -> Result:
        return cls(error=error)
