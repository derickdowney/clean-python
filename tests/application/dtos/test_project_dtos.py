import pytest

from clean_python.application.dtos.project_dtos import CompleteProjectRequest
from clean_python.domain.exceptions import ValidationError


def test_CompleteProjectRequest_init_requires_string_for_UUID():
    with pytest.raises(TypeError):
        CompleteProjectRequest()


def test_CompleteProjectRequest_can_init_with_completion_notes():
    CompleteProjectRequest("project_id", "these are some completion notes")


def test_CompleteProjectRequest_with_empty_project_id_raises_ValidationError():
    with pytest.raises(ValidationError):
        CompleteProjectRequest("   ")
