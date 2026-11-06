from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
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
    allow_due_date_in_past: bool = False  # for pytest testing purposes

    def __post_init__(self):
        if self.due_date < datetime.now() and not self.allow_due_date_in_past:
            raise ValueError("Deadline cannot be in the past")

    def is_overdue(self) -> bool:
        return datetime.now() > self.due_date

    def time_remaining(self) -> timedelta:
        return max(timedelta(0), self.due_date - datetime.now())
