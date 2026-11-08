from clean_python.domain.entities.task import Task
from tests.domain.repositories.fakes import FakeTaskRepository


def test_TaskRepository_enables_save_and_get_contracts():
    task_repo: FakeTaskRepository = FakeTaskRepository()
    task: Task = Task("t", "d")
    task_repo.save(task)
    assert task_repo.get(str(task.id)) == task
