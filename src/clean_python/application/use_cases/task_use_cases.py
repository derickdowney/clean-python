from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from clean_python.application.common.result import Error, Result
from clean_python.application.service_ports.notifications import NotificationPort
from clean_python.domain.entities.task import Task
from clean_python.domain.exceptions import TaskNotFoundError, ValidationError
from clean_python.domain.repositories.task_repository import TaskRepository


@dataclass(frozen=True)
class CompleteTaskUseCase:
    """Use case for marking a task as complete and notifying stakeholders"""

    task_repository: TaskRepository

    def execute(self, task_id: UUID, completion_notes: str | None = None) -> Result:
        try:
            # TODO: Validate input here

            task: Task = self.task_repository.get(str(task_id))
            task.complete(notes=completion_notes)
            self.task_repository.save(task)

            # TODO: To make LSP error go away, we'd need to confirm
            # "task.completed_at" is not "None" first.

            # Return simplified task data
            return Result.success(
                {
                    "id": str(task.id),
                    "status": "completed",
                    "completion_date": task.completed_at.isoformat(),
                }
            )
        except TaskNotFoundError:
            return Result.failure(Error.not_found("Task", str(task_id)))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))


@dataclass(frozen=True)
class TaskManagementUseCase:
    task_repository: TaskRepository
    notification_service: NotificationPort
    _optional_services: dict[str, Any] = field(default_factory=dict)

    def register_service(self, name: str, service: Any) -> None:
        """Register an optional service"""
        self._optional_services[name] = service

    def complete_task(self, task_id: UUID) -> Result:
        try:
            # task = self.task_repository.get(task_id)
            # task.complete()
            # self.task_repository.save(task)

            # Required notification service
            # self.notification_service.notify_task_completed(task)

            # Optional integrations
            if analytics := self._optional_services.get("analytics"):
                analytics.track_task_completion(task_id)
            if audit := self._optional_services.get("audit"):
                audit.log_task_completion(task_id)

            # return Result.sucess(TaskResponse.from_entity(task))
            return Result.success("success")
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
