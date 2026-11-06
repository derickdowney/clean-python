from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta
from enum import Enum

import pytest

from clean_python.domain.value_objects import Deadline, Priority, TaskStatus


def test_TaskStatus_is_Enum_type():
    assert isinstance(TaskStatus.TODO, Enum)


def test_Priority_is_Enum_type():
    assert isinstance(Priority.LOW, Enum)


one_week_later: datetime = datetime.now() + timedelta(days=7)


def test_Deadline_init_requires_due_date_datetime_arg():
    with pytest.raises(TypeError):
        Deadline()
    Deadline(one_week_later)


def test_Deadline_due_date_is_frozen():
    with pytest.raises(FrozenInstanceError):
        deadline: Deadline = Deadline(one_week_later)
        deadline.due_date += timedelta(days=30)


def test_Deadline_due_date_cannot_be_init_with_date_in_past():
    with pytest.raises(ValueError):
        Deadline(datetime(1999, 1, 1))
