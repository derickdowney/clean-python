I asked ChatGPT for feedback on my TDD code. It had the following advice.

# Major Takeaway
- Instantiate objects directly in constructor/init tests
- Use object factory in behavior tests
- A failing testing suite can be good.
    - It can reveal that a fundamental contract has changed.
- UPDATE!!!! Sam Keen says to use a fixture instead! See section # PYTEST FIXTURES!


# Use a Factory when Instantiation Is Not Important
I am doing the following all over: `task: Task = Task("t", "d")`
However, if we add a new required argument to Task, then all of these
tests would fail for reasons different than why the test exists!!!

**"Tests should construct their test subjects through a common factory whenever
the specific construction details aren't relevant to the test."**

"This is sometimes called a Test Data Builder or Object Mother pattern.
You don't need to formally implement either pattern, though.
A simple helper function is perfectly adequate."


# Don't use Factory when Testing Construction!!!
For tests like `test_Task_init_requires...`, do NOT use the factory!!!
When you are specifically testing initialization, then you should
initialize the real way!

**Don't try to prevent all tests from breaking.
Try to prevent unrelated tests from breaking.**


# Add Flexibility to Factory
Allow for defaults, but allow for keyword-arg overrides when needed:
```Python
def create_task(
    *,
    title: str = "title",
    description: str = "description",
    due_date: Deadline | None = None,
    priority: Priority = Priority.MEDIUM,
) -> Task:
    """Creates a valid Task() instance."""
    return Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
    )
```


#
#
# Beginning Testing Notes from Chapter 8 of "Clean Architecture with Python"
#
#

# Testing and Clean Architecture
Tightly coupled complex systems rely on brittle and slow "end-to-end" tests.
Clean Architecture makes it easy to rely mostly on unit and integration tests.
"...Clean Architecture enables us to build substantial confidence in our system
through focused unit and integration tests alone." p. 189

Unit tests = fast and a lot of them
Integration tests = not as fast and not as many.
 - Tests interactions between components.
End-to-end tests = small number to verify critical user workflows
- Typically provide less precise feedback when failures occur

Clean Architecture makes setup slow at first, and testing extremely easy later.
Coupled architectures make setup fast, then testing extremely hard later.

# Tests as Clients
**Tests are clients of our code.**
"If we find that our tests are difficult to write or require complex setup,
this often signals that our production code needs improvement...
These signals serve as early warnings, helping us identify and correct
architectural violations before they become deeply embedded in our codebase."
p. 190

# Arrange-Act-Assert (AAA) Pattern
Proposed by Bill Wake in 2011:
https://xp123.com/3a-arrange-act-assert/

Sam Keen lays out tests with AAA comments like:
```Python
def test_something():
    """Test that tests something"""
    # Arrange
    task = Task()

    # Act
    task.something()

    # Assert
    assert task.something is not None
```

# Test Double Tools in Python, and Mocks
**Test Doubles** act as dependency replacements for components under test.
Python's `unittest.mock` library provides powerful tools for creating test
doubles, and integrates seamlessly with `pytest`

```Python
from unittest.mock import Mock

# Create a mock object that records calls and can return preset values
mock_repo = Mock()
# Configure the response we want
mock_repo.get.return_value = some_task
# Call will return some_task
mock_repo.get(123)
# Verify the call happened exactly once
mock_repo.get.assert_called_once()

# Mocks track all interaction details
# Shows what arguments were passed
print(mock_repo.get.call_args)
# Shows how many times it was called
print(mock_repo.get.call_count)
```

# Mocks Instead of Dependencies
A "task completion" use case requires both a repository to persist change
and a notification service to alert stakeholders. **Both of these can be mocks!**

```Python
def test_successful_task_completion():
    """Test task completion using mock dependencies."""
    # Arrange
    task = Task(
        title="Test task",
        description="Test description",
        project_id=UUID('12345678-1234-5678-1234-567812345678'),
    )
    task_repo = Mock()
    task_repo.get.return_value = task
    notification_service = Mock()

    use_case = CompleteTaskUseCase(
        task_repository=task_repo,
        notification_service=notification_service
    )
    request = CompleteTaskrequest(task_id=str(task.id))

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.is_success
    task_repo.save.assert_called_once_with(task)
    notification_service
        .notify_task_completed
        .assert_called_once_with(task)
```

# Testing Data Translation of Interface Adapters
## Loose Mock vs Strict Mock
When you pass a class into the `spec` arg of the `Mock` class, then the mock
will only let you call methods actually within that passed-in class!
This enables us to "catch not just behavioral issues but also contract violations!"
(p. 199)

```Python
class MyClass:
    def existing_method(self):
        pass

loose_mock = Mock()
loose_mock.existing_method() # No error raised
loose_mock.non_existent_method() # No error raised

strict_mock = Mock(spec=MyClass)
strict_mock.existing_method() # No error raised
strict_mock.non_existent_method() # Raises AttributeError
```
## Interface Adapter Test
Example here: https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_8/TodoApp/tests/interface/controller/test_task_controller.py


## Presenter Tests
This test ensures proper formatting of task completion dates into human-readable
strings for CLI:
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_8/TodoApp/tests/interface/presenters/test_cli.py

Notice that this test allows us to test everything with no mocks! We just use
the `CliTaskPresenter()` dependency directly since that's what we're testing.
This test is not entangled with anything involving business rules, persistence,
or anything else!

In the link above, the top test just tests the "completion time" formatting.
However the bottom test tests **the entire presenter output in one test!**

# Integration Tests (Across Architectural Boundaries)
"Rather than exhaustively testing every combination of components, we focus on
key boundary crossings, particularly those involving infrastructure like
persistence or external services." p 201

## Pytest Fixtures as Factories, and tmp_path
Use `@pytest.fixture` to create a factory helper function?
The `tmp_path` variable is a **pytest builtin** for temp dirs during tests.
By putting it as an arg in a method, then pytest generates a unique temporary
path for your test.
```Python
@pytest.fixture
def repository(tmp_path): 
    """Create repository using temporary path as data_dir"""
    return FileTaskRepository(data_dir=tmp_path)
```

## File System Repository Test using Fixtures
The example in the book is wrong, so here's a Gemini-generated test that
leverages a fixture like the one above. Notice how **fixtures can be
passed into pytest tests as an argument!!** No need to call `repositories()`
function within the `test_` function. Instead just pass `repositories` in
as an argument.
```Python
@pytest.fixture
def repositories(tmp_path):
    """Provide both connected task and project repositories."""
    task_repo = FileTaskRepository(tmp_path)
    project_repo = FileProjectRepository(tmp_path)
    project_repo.set_task_repository(task_repo)
    return task_repo, project_repo


def test_repo_handles_project_task_relationships(repositories):
    """Integration test verifying repository handles entity relationships."""
    task_repo, project_repo = repositories

    # Create project and tasks through the repository
    project = Project(name="Test Project", description="Testing relationships")
    project_repo.save(project)

    task = Task(title="Test Task", description="Testing relationships", project_id=project.id)
    task_repo.save(task)

    # Act - Load project with its tasks
    loaded_project = project_repo.get(project.id)

    # Assert
    assert len(loaded_project.tasks) == 1
    assert loaded_project.tasks[0].title == "Test Task"
```


## Architectural Guarantees
An example of an "architectural guarantee" is that the Todo app creates and
persists the "inbox" project automatically.
He uses an integration test that has two separate repository instances
pointing to the same data directory. (I don't understand though...)


## Task Persistence
First, he has a unit test for task creation where all dependencies are mocked.
Then, he has an integration test that confirms that task creation ACTUALLY
persists into a database:
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_8/chapter_code_excerpts/10_def%20test_task_creation_with_persistence.py
However, he's still mocking the `notification_service` since this is just testing
persistence!

# Tools and Patterns for Test Maintenance

## Test Dependencies
`domain` tests shouldn't need to import anything from `application` layers
or higher.

## Using Parameterized Tests
A **parameterized test** allows you to run the same test function over and over
with different parameters each time. This makes it so that you can, for example,
run a test under 10 different conditions, and catch an error specifically with
just test run #7.

Notice how `request_data` is entering the method as a dictionary, and thus
you need to use the unpacking `**request_data` syntax to assign the entries
to parameters for the `CreateTaskRequest()`.

Using the `ids` parameter makes test failures more meaningful.
In the code below, instead of seeing a failure with:
    - `test_task_creation_scenarios[0]`
Pytest will instead show us a failure with:
    - `test_task_creation_scenarios[basic-task]`

Example of a parameterized test:
```Python
from uuid import UUID
import pytest
from unittest.mock import Mock


@pytest.mark.parametrize(
    "request_data,expected_behavior",
    [
        # basic-task (defaults to inbox)
        (
            # request_data
            {"title": "Test Task", "description": "Basic creation"},

            # expected_behavior
            {"project_type": ProjectType.INBOX, "priority": Priority.MEDIUM}
        ),

        # project-task (assigned to specific project)
        (
            # request data
            {
                "title": "Project Task",
                "description": "With project",
                "project_id": "project-uuid"
            }, 

            # expected_behavior
            {"project_type": ProjectType.REGULAR, "priority": Priority.MEDIUM}
        ),
        # priority-task
        # ... data for task
    ],
    ids=["basic-task", "project-task", "priority-task"]
)
def test_task_creation_scenarios(request_data, expected_behavior):
    """Test task creation use case handles various input scenarios correctly."""
    # Arrange
    task_repo = Mock(spec=TaskRepository)
    project_repo = FileProjectRepository(tmp_path)  # Real project repo for INBOX
    
    use_case = CreateTaskUseCase(
        task_repository=task_repo,
        project_repository=project_repo
    )
    
    # Act
    result = use_case.execute(CreateTaskRequest(**request_data))
    
    # Assert
    assert result.is_success
    created_task = result.value
    if expected_behavior["project_type"] == ProjectType.INBOX:
        assert UUID(created_task.project_id) == project_repo.get_inbox().id
    assert created_task.priority == expected_behavior["priority"]
```

# PYTEST FIXTURES!
As our testing suite grows:
- Domain tests require clean entity instances
- Use case tests need properly configured repositories and services
- Interface tests need formatted request data
The `pytest` fixture system paired with `conftest.py` files helps address these!

Fixtures make it so your test stays focused on **behavior** not setup!!
Plus if something changes in your system, you just update the fixture.

You can have multiple `conftest.py` files in multiple directories.
Their contents are inherited by all directories at that level and below.
`tests/conftest.py` is used by all tests.
`tests/domain/entities/conftest.py` is only used by Entity tests.

**Fixtures must respect architectural boundaries!**
Fixtures should only depend on inner layers, just like our app architecture!
Application fixtures can depend on Domain fixtures, but not vice versa.

```Python
# test/conftest.py - Root fixtures available to all tests
@pytest.fixture
def sample_task_data():
    """Provide basic task attributes for testing"""
    return {
        "title": "Test Task",
        "description": "Sample task for testing",
        "project_id": UUID('12345678-1234-5678-1234-567812345678'),
    }

# tests/domain/conftest.py - Domain layer fixtures
@pytest.fixture
def domain_task(sample_task_data):
    """Provide a clean Task entity for domain tests."""
    return Task(**sample_task_data)
```

# Freezegun for controlling time!
Testing deadline calculations or time-based notifications requires careful
handling of time. Instead of manipulating system time (which could potentially
affect other tests), we can use the `freezegun` library.

`freezegun` provides a context manager that sets a specific time:
```Python
def test_task_deadline_approaching():
    """Test deadline notifications respect time boundaries."""
    # Arrange
    with freeze_time("2024-01-14 12:00:00"):
        task = Task(
            ...
            # due date set for 2024-01-15
            )

    # Act
    with freeze_time("2024-01-14 13:00:00"):
        result = use_case.execute()

    # Assert
    assert result.is_success
    notification_service.notify_task_deadline_approaching_assert_called_once()
```

# Run tests in random order with `pytest-random-order`
There might be hidden dependencies in your tests.
For example, the `notification_service` may keep a list of all pending
notifications, which impacts other tests.
Running tests in random order helps reveal these dependencies.

To address this:
    `pip install pytest-random-order` or `uv add pytest-random-order`

Configure on every test:
```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--random-order"
```

After a test fails, you can force the same ordering by passing in a seed value:
`pytest --random-order-seed=123456`


You'll know seed because it says it at top like:
```
================================== test session starts ===================================
platform darwin -- Python 3.15.0, pytest-9.2.0, pluggy-1.7.0
Using --random-order-bucket=module
Using --random-order-seed=557366
```

# Running tests in parallel
Install `uv add pytest-xdist` to run tests in parallel and speed things up!

Add the `-n auto` option to your `pytest` call to enable parallel tests:
```toml
[tool.pytest.ini_options]
addopts = "--random-order -n auto" # random order AND parallel execution
```
This says "the number of CPU cores is automatically determined."

Use `@pytest.mark.serial` to mark tests that must run sequentially
Use `@pytest.mark.resource_group('global-cache')` to share test resources
(I don't understand how either of these work, would need to investigate later)

Without `pytest-xdist` installed, my 60 tests take 0.27 seconds
With it installed, my 60 tests take 0.06 seconds
