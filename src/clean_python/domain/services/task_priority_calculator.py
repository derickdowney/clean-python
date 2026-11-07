from datetime import timedelta

from clean_python.domain.entities.task import Task
from clean_python.domain.value_objects import Priority


class TaskPriorityCalculator:
    @staticmethod
    def calculate_priority(task: Task):
        if task.is_overdue():
            return Priority.HIGH
        elif task.due_date and task.due_date.time_remaining() <= timedelta(days=2):
            return Priority.MEDIUM
        else:
            return Priority.LOW
