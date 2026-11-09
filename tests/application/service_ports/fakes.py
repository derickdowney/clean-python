from uuid import UUID

from clean_python.application.service_ports.notifications import NotificationService
from clean_python.domain.entities.task import Task


class FakeNotificationService(NotificationService):
    """Fake notfication service for testing"""

    def notify_task_assigned(self, task_id: UUID) -> None:
        self.last_task_assigned: UUID = task_id

    def notify_task_completed(self, task: Task) -> None:
        self.last_task_completed: UUID = task.id
