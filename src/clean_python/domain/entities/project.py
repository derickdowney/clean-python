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
