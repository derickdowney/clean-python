from uuid import uuid4

import pytest

from clean_python.domain.entities.project import Project
from clean_python.domain.entities.task import Task

"""
Note about TypeError vs. ValueError from Python's documentation:

Passing arguments of the wrong type (e.g. passing a list when an int is
expected) should result in a TypeError, but passing arguments with the wrong
value (e.g. a number outside expected boundaries) should result in a ValueError.

From Gemini:
    **TypeError (The "Structure / Shape" Error)**
    A TypeError is raised when an operation, function call, or method is
    performed with the wrong number of arguments, the wrong types of arguments,
    or on an object that doesn't support the operation.

    **ValueError (The "Content" Error)**
    A ValueError is raised when Python successfully receives the correct number
    of arguments and the correct types (e.g., they are both strings), but the
    actual value of the data is invalid for your business logic.
"""


def test_Project_init_requires_a_name_during_init():
    with pytest.raises(TypeError):
        Project()
    with pytest.raises(TypeError):
        Project(description="desc")


def test_Project_name_and_description_are_accessible():
    project: Project = Project("someName", "someDescription")
    assert project.name == "someName"
    assert project.description == "someDescription"


def test_Project_name_and_description_are_mutable():
    project: Project = Project("name", "desc")
    project.name = "newName"
    assert project.name == "newName"

    project.description = "newDesc"
    assert project.description == "newDesc"


def test_Project_tasks_property_returns_list_of_all_tasks_in__tasks_dict():
    project: Project = Project("name", "desc")

    task1: Task = Task("t1", "d1")
    project._tasks[task1.id] = task1

    task2: Task = Task("t2", "d2")
    project._tasks[task2.id] = task2

    tasks: list[Task] = project.tasks
    assert task1 in tasks
    assert task2 in tasks
