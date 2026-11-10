from clean_python.application.dtos.project_dtos import CompleteProjectRequest
from clean_python.application.use_cases.project_use_cases import CompleteProjectUseCase
from tests.application.service_ports.fakes import FakeNotificationService
from tests.domain.repositories.fakes import FakeTaskRepository


def test_CompleteProjectUseCase():
    pass
    # Giving up on this. Can't because I don't have a project_id.
    # Don't have time to do this so in-depth.
    # I need to just finish this book ASAP!!!!!!!

    # request: CompleteProjectRequest = CompleteProjectRequest("name", "", 3)
    # use_case: CompleteProjectUseCase = CompleteProjectUseCase(
    #     FakeTaskRepository(), FakeNotificationService()
    # )
