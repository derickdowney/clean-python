from clean_python.domain.entities.task import Task
from clean_python.domain.value_objects import Priority


class TaskPriorityCalculator:
    @staticmethod
    def calculate_priority(task: Task):
        return Priority.HIGH
