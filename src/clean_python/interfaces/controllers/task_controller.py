from dataclasses import dataclass

from clean_python.application.use_cases.task_use_cases import CompleteTaskUseCase


@dataclass
class TaskController:
    complete_task_use_case: CompleteTaskUseCase
    presenter: TaskPresenter
