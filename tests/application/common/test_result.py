from clean_python.application.common.result import Error, ErrorCode, Result
from clean_python.domain.entities.task import Task


def test_create_Result_failure_with_NOT_FOUND_error():
    task: Task = Task("t", "d")
    entity_type = str(type(task))
    entity_id = str(task.id)
    failure: Result = Result.failure(Error.not_found(entity_type, entity_id))
    assert failure.error is not None
    assert failure.error.code == ErrorCode.NOT_FOUND
    assert failure.error.details is None
    assert failure.is_success == False


def test_create_Result_failure_with_VALIDATION_ERROR_error():
    failure: Result = Result.failure(Error.validation_error("invalid"))
    assert failure.error is not None
    assert failure.error.code == ErrorCode.VALIDATION_ERROR
    assert failure.error.message == "invalid"
    assert failure.error.details is None
    assert failure.is_success == False


def test_create_Result_success():
    success: Result = Result.success("response")
    assert success.is_success == True
    assert success.value == "response"
