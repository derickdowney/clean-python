from dataclasses import dataclass, field
from uuid import UUID

from clean_python.domain.entities.task import Task


@dataclass(eq=False)
class Project:
    name: str
    description: str = ""
    _tasks: dict[UUID, Task] = field(default_factory=dict, init=False)

    @property
    def tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def add_task(self, task: Task) -> None:
        self._tasks[task.id] = task

    # Note: Standard practice in Python is:
    #   - Use "dict.del()" if you want KeyError raised if key is missing
    #   - Use "dict.pop()" if you want no errors raised if key is missing
    def remove_task(self, task_id: UUID) -> None:
        del self._tasks[task_id]
        # self._tasks.pop(task_id, None)
