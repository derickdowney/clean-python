from datetime import datetime, timedelta

from clean_python.domain.entities.task import Task
from clean_python.domain.value_objects import Deadline, Priority


def test_Task_init_requires_title_and_description():
    assert Task("some title", "some description")


def test_Task_init_optionally_allows_due_date():
    assert Task("t", "d", Deadline(datetime.now() + timedelta(days=7)))


def test_Task_inits_by_default_with_medium_priority():
    assert Task("t", "d").priority == Priority.MEDIUM
