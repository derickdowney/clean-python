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

    @classmethod
    def validation_error(cls, message: str) -> Error:
        return cls(code=ErrorCode.VALIDATION_ERROR, message=message)


@dataclass(frozen=True)
class Result:
    """Represents success or failure of a use case execution

    Note that this can be used to translate domain-specific errors into
    uniform application-level errors."""

    value: Any = None
    error: Error | None = None

    """
        Note about Python:
            - Use "property" when checking state, even if no local variable
            - Use a method when doing an action or behavior
    """

    @property
    def is_success(self) -> bool:
        return self.error is None

    @classmethod
    def success(cls, value: Any) -> Result:
        return cls(value=value)

    @classmethod
    def failure(cls, error: Error) -> Result:
        return cls(error=error)
