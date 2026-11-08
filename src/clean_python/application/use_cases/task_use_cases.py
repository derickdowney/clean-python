from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from clean_python.application.common.result import Error, Result
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
