import pytest

from clean_python.application.dtos.project_dtos import CompleteProjectRequest


def test_CompleteProjectRequest_init_requires_string_for_UUID():
    with pytest.raises(TypeError):
        CompleteProjectRequest()
