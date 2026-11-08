from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from clean_python.domain.entities.entity import Entity
from clean_python.domain.value_objects import Deadline, Priority, TaskStatus


@dataclass
class Task(Entity):
    title: str
    description: str
    due_date: Deadline | None = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)
    completed_at: datetime | None = field(default=None, init=False)
    completion_notes: str | None = field(default=None, init=False)
    project_id: UUID | None = field(default=None, init=False)

    """
    To perform additional initialization operations after @dataclass's
    standard __init__ operations, use the __post_init__ dunder method.
    """

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

    """
    To create additional constructors for your @dataclass beyond just __init__,
    use the @classmethod decorator and return a `cls(...)` instance.
    """

    @classmethod
    def create_urgent_task(
        cls, title: str, description: str, due_date: Deadline | None = None
    ):
        return cls(title, description, due_date, Priority.HIGH)

    """
    These methods below are called "business rules" or "invariants."
    They are logic that is enforced at the entity level.

    There's a difference between "entity-level rules" like the ones below,
    and "domain-level rules." For example, a rule like "a user can't have more
    than five high-priority tasks at one time" would involve multiple tasks and
    possibly user settings, so this would not belong in the Task entity.
    """

    def start(self) -> None:
        if self.status != TaskStatus.TODO:
            raise ValueError("Only tasks with 'TODO' status can be started")
        self.status = TaskStatus.IN_PROGRESS

    def complete(self, notes: str | None = None) -> None:
        if self.status == TaskStatus.DONE:
            raise ValueError("Task is already completed")
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.completion_notes = notes

    def is_overdue(self) -> bool:
        return self.due_date is not None and self.due_date.is_overdue()
