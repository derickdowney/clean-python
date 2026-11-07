from dataclasses import dataclass, field

from clean_python.domain.entities.entity import Entity
from clean_python.domain.value_objects import Deadline, Priority, TaskStatus


@dataclass
class Task(Entity):
    title: str
    description: str
    due_date: Deadline | None = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)

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

    def complete(self) -> None:
        if self.status == TaskStatus.DONE:
            raise ValueError("Task is already completed")
        self.status = TaskStatus.DONE

    def is_overdue(self) -> bool:
        return self.due_date is not None and self.due_date.is_overdue()
