from abc import ABC, abstractmethod
from uuid import UUID

from clean_python.domain.entities.task import Task


class NotificationPort(ABC):
    """Service port for sending notifications"""

    @abstractmethod
    def notify_task_assigned(self, task_id: UUID) -> None:
        """Notify when a task is assigned"""
        pass

    @abstractmethod
    def notify_task_completed(self, task: Task) -> None:
        """Notify when a task is completed"""
        pass
