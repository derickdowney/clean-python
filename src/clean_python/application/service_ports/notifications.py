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


class FancyEmailNotificationService:
    """Third-party service named 'Fancy Email' with its own interface"""

    def send_notification(self, payload: dict) -> None:
        # Modern service implementation
        pass


class FancyEmailNotificationAdapter(NotificationPort):
    """Adapts the 'Fancy Email' service to work with our interface"""

    def __init__(self, fancy_service: FancyEmailNotificationService):
        self._service = fancy_service

    def notify_task_completed(self, task: Task) -> None:
        self._service.send_notification(
            {"type": "TASK_COMPLETED", "taskId": str(task.id)}
        )
