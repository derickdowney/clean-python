from clean_python.domain.entities.task import Task
from clean_python.domain.repositories.task_repository import TaskRepository


class FakeTaskRepository(TaskRepository):
    """An in-memory task repository for testing purposes only"""

    def __init__(self):
        self._repo = {}

    def save(self, task: Task):
        self._repo[str(task.id)] = task

    def get(self, task_id: str) -> Task:
        return self._repo[task_id]
