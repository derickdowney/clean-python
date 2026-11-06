from dataclasses import dataclass

from clean_python.domain.entities.entity import Entity


@dataclass
class Task(Entity):
    title: str
    description: str
