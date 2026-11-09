from clean_python.domain.entities.task import Task
from tests.application.service_ports.fakes import FakeNotificationService


def test_FakeNotificationService():
    service: FakeNotificationService = FakeNotificationService()
    task_to_assign: Task = Task("t", "d")
    task_to_complete: Task = Task("t", "d")
    service.notify_task_assigned(task_to_assign.id)
    service.notify_task_completed(task_to_complete)
    assert task_to_assign.id == service.last_task_assigned
    assert task_to_complete.id == service.last_task_completed
