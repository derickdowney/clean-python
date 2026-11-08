from clean_python.domain.entities.task import Task
from clean_python.domain.repositories.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._repo = {}

    def save(self, task: Task):
        self._repo[str(task.id)] = task

    def get(self, task_id: str) -> Task:
        return self._repo[task_id]


def test_TaskRepository_enables_save_and_get_contracts():
    task_repo: InMemoryTaskRepository = InMemoryTaskRepository()
    task: Task = Task("t", "d")
    task_repo.save(task)
    assert task_repo.get(str(task.id)) == task
