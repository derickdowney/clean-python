import random

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


def test_CompleteProjectRequest_raises_ValidationError_long_completion_notes():
    with pytest.raises(ValidationError):
        note_1001_chars_long: str = "".join(random.choices("abc", k=1001))
        CompleteProjectRequest("project_id", note_1001_chars_long)
