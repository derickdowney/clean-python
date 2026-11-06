from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(frozen=True)
class Deadline:
    due_date: datetime

    def __post_init__(self):
        if self.due_date < datetime.now():
            raise ValueError("Deadline cannot be in the past")
