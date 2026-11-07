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

    def start(self) -> None:
        if self.status != TaskStatus.TODO:
            raise ValueError("Only tasks with 'TODO' status can be started")
        self.status = TaskStatus.IN_PROGRESS
