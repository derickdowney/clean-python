from dataclasses import dataclass

from clean_python.application.common.result import Error, Result
from clean_python.application.dtos.project_dtos import (
    CompleteProjectRequest,
    CompleteProjectResponse,
)
from clean_python.application.service_ports.notifications import NotificationPort
from clean_python.domain.entities.project import Project
from clean_python.domain.exceptions import ProjectNotFoundError, ValidationError
from clean_python.domain.repositories.task_repository import TaskRepository


@dataclass(frozen=True)
class CompleteProjectUseCase:
    task_repo: TaskRepository
    notification_service: NotificationPort

    # Uses CompleteProjectRequest instead of discreet parameters
    def execute(self, request: CompleteProjectRequest) -> Result:
        try:
            params = request.to_execution_params()

            # TODO: project = self.project_repository.get(params["project_id"])
            project: Project = Project("some name")
            # TODO: project.mark_completed(notes=params["completion_notes"])
            # TODO: complete all outstanding tasks
            # TODO: project_repository.save(project)

            # Returning CompleteProjectResponse instead of handbuilt dict
            response = CompleteProjectResponse.from_entity(project)
            return Result.success(response)
        except ProjectNotFoundError:
            return Result.failure(Error.not_found("Project", str(params["name"])))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
