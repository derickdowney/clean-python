from datetime import datetime, timedelta

from clean_python.domain.entities.task import Task
from clean_python.domain.services.task_priority_calculator import TaskPriorityCalculator
from clean_python.domain.value_objects import Deadline, Priority
from tests.domain.test_value_objects import one_week_earlier, one_week_later


def test_TaskPriorityCalculator_returns_high_priority_if_task_is_overdue():
    task: Task = Task("t", "d")
    task.due_date = Deadline(one_week_earlier, True)
    assert TaskPriorityCalculator.calculate_priority(task) == Priority.HIGH


def test_calculator_returns_medium_priority_if_two_days_remaining():
    task: Task = Task("t", "d")
    task.due_date = Deadline(datetime.now() + timedelta(hours=36))
    assert TaskPriorityCalculator.calculate_priority(task) == Priority.MEDIUM


def test_calculator_returns_low_priority_if_due_in_more_than_two_days():
    task: Task = Task("t", "d")
    task.due_date = Deadline(one_week_later, True)
    assert TaskPriorityCalculator.calculate_priority(task) == Priority.LOW
