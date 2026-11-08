"""
    The "factory pattern" is when you create a "factory" class instance whose
    role is to produce instances of another class.

    Since DDD wants clear boundaries between all entities, a "factory" might
    be appropriate for when you need those entities to interact with each other.

    Factories might be appropriate when:
        - An object requires setting up relationships with other objects
        - Entity creation requires external dependencies
        - You need different subclasses based on runtime conditions

    However, you might also be able to accomplish all of this using an
    Application Service or a Domain Service.

    Here's an example of a "TaskFactory":


from uuid import UUID

from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import Priority


class TaskFactory:
    def __init__(self, user_service, project_repository):
        self.user_service = user_service
        self.project_repository = project_repository

    def create_task_in_project(
        self, title: str, description: str, project_id: UUID, assignee_id: UUID
    ):
        project = self.project_repository.get_by_id(project_id)
        assignee = self.user_service.get_user(assignee_id)

        task = Task(title, description)
        task.project = project
        task.assignee = assignee

        if project.is_high_priority() and assignee.is_manager():
            task.priority = Priority.HIGH

        project.add_task(task)
        return task
"""
