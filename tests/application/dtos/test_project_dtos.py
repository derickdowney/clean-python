import random
from typing import Any
from uuid import UUID, uuid4

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


def test_CompleteProjectRequest_to_execution_params_converts_str_to_UUID():
    id: UUID = uuid4()
    request: CompleteProjectRequest = CompleteProjectRequest(str(id))
    exec_params: dict[str, Any] = request.to_execution_params()
    assert exec_params["project_id"]
    assert type(exec_params["project_id"]) == UUID
    assert exec_params["project_id"] == id
