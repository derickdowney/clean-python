from clean_python.application.common.result import Result
from clean_python.application.use_cases.task_use_cases import CompleteTaskUseCase
from clean_python.domain.entities.task import Task
from clean_python.domain.value_objects import TaskStatus
from tests.domain.repositories.fakes import FakeTaskRepository


def test_CompleteTaskUseCase():
    task_repo: FakeTaskRepository = FakeTaskRepository()

    taskBeforeUseCase: Task = Task("t", "d")
    assert taskBeforeUseCase.status == TaskStatus.TODO

    task_id = taskBeforeUseCase.id
    task_repo.save(taskBeforeUseCase)

    use_case: CompleteTaskUseCase = CompleteTaskUseCase(task_repo)
    response: Result = use_case.execute(task_id)
    response_value: dict[str, str] = response.value
    assert response_value["id"] == str(task_id)
    assert response_value["status"] == "completed"

    taskAfterUseCase: Task = task_repo.get(str(task_id))
    assert taskAfterUseCase.status == TaskStatus.DONE
