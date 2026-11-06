from dataclasses import FrozenInstanceError
from datetime import datetime
from enum import Enum

import pytest

from clean_python.domain.value_objects import Deadline, Priority, TaskStatus


def test_TaskStatus_is_Enum_type():
    assert isinstance(TaskStatus.TODO, Enum)


def test_Priority_is_Enum_type():
    assert isinstance(Priority.LOW, Enum)


def test_Deadline_init_requires_due_date_datetime_arg():
    with pytest.raises(TypeError):
        Deadline()
    Deadline(datetime.now())


def test_Deadline_due_date_is_frozen():
    with pytest.raises(FrozenInstanceError):
        deadline: Deadline = Deadline(datetime(1999, 1, 1))
        deadline.due_date = datetime.now()
