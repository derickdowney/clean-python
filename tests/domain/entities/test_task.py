from datetime import datetime, timedelta

import pytest

from clean_python.domain.entities.task import Task
from clean_python.domain.value_objects import Deadline, Priority, TaskStatus


# Helper Functions
def create_task() -> Task:
    """Creates a valid Task() instance"""
    return Task("title", "description")


# Tests
def test_Task_init_requires_title_and_description():
    assert Task("some title", "some description")


def test_Task_init_optionally_allows_due_date():
    assert Task("t", "d", Deadline(datetime.now() + timedelta(days=7)))


def test_Task_inits_by_default_with_medium_priority():
    assert Task("t", "d").priority == Priority.MEDIUM


def test_Task_priority_can_be_set_during_init():
    assert Task("t", "d", priority=Priority.HIGH).priority == Priority.HIGH


def test_Task_priority_is_mutable():
    task: Task = Task("t", "d", priority=Priority.HIGH)
    task.priority = Priority.LOW
    assert task.priority == Priority.LOW


def test_Task_inits_by_default_with_status_TaskStatus_TODO():
    assert Task("t", "d").status == TaskStatus.TODO


def test_Task_status_cannot_be_set_during_init():
    with pytest.raises(TypeError):
        Task("t", "d", status=TaskStatus.IN_PROGRESS)


def test_Task_status_is_mutable():
    task: Task = Task("t", "d")
    task.status = TaskStatus.DONE
    assert task.status == TaskStatus.DONE


def test_Task_start_sets_status_to_IN_PROGRESS():
    task: Task = Task("t", "d")
    task.start()
    assert task.status == TaskStatus.IN_PROGRESS


def test_Task_start_throws_ValueError_if_not_in_TODO_status():
    task: Task = Task("t", "d")
    task.status = TaskStatus.IN_PROGRESS
    with pytest.raises(ValueError):
        task.start()


def test_Task_complete_sets_status_to_DONE():
    task: Task = create_task()
    task.complete()
    assert task.status == TaskStatus.DONE


def test_Task_complete_raises_ValueError_if_already_in_DONE_status():
    task: Task = create_task()
    task.status = TaskStatus.DONE
    with pytest.raises(ValueError):
        task.complete()
