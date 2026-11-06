from enum import Enum

from clean_python.domain.value_objects import Priority, TaskStatus


def test_TaskStatus_is_Enum_type():
    assert isinstance(TaskStatus.TODO, Enum)


def test_Priority_is_Enum_type():
    assert isinstance(Priority.LOW, Enum)
