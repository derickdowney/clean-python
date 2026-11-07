from clean_python.domain.entities.task import Task
from clean_python.domain.services.task_priority_calculator import TaskPriorityCalculator
from clean_python.domain.value_objects import Deadline, Priority
from tests.domain.test_value_objects import one_week_earlier


def test_TaskPriorityCalculator_returns_high_priority_if_task_is_overdue():
    task: Task = Task("t", "d")
    task.due_date = Deadline(one_week_earlier, True)
    assert TaskPriorityCalculator.calculate_priority(task) == Priority.HIGH
