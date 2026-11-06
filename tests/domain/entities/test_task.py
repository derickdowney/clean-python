from clean_python.domain.entities.task import Task


def test_Task_requires_title_and_description_for_init():
    assert Task("some title", "some description")
