from dataclasses import dataclass, field

from clean_python.domain.entities.entity import Entity
from clean_python.domain.value_objects import Deadline, Priority, TaskStatus


@dataclass
class Task(Entity):
    title: str
    description: str
    due_date: Deadline | None = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO)
