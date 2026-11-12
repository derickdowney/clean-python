# Overview
The "Frameworks and Drivers layer" is outermost ring of Clean Architecture.
These are "the details" of our system as opposed to "core business logic".

# Key Principles of Frameworks and Drivers Layer
- External Boundary: Handles all interactions with outside world, including
    - User interfaces (CLI, web, API endpoints)
    - Database systems (drivers like SQLite; frameworks like SQLAlchemy)
    - External services and APIs
    - File systems and device interactions
- Dependency Direction: All dependencies point inward, never outward
- Implementation Details: Contains exact choice of databases/frameworks/etc.

# Frameworks vs. Drivers
## Frameworks
Frameworks are comprehensive software platforms that impose their own
architectural and control flow. Examples:
- Web frameworks like Flash or FastAPI
- CLI frameworks like Click or Typer
- Object relational modeling (ORM) frameworks like SQLAlchemy

These often require complex Interface Adapter layer components:
- Controllers transform framework-specific requests into use case inputs
- Presenters format domain data for framework consumption
- View models structure data appropriately for framework display

Framework API code example:
```Python
@app.route("/tasks", methods["POST"])
def create_task():
    """Framework requires full Interface Adapters stack"""
    result = task_controller.handle_create(
        title=request.json["title"],
        description=request.json["description"]
    )
    return task_presenter.present(result)
```

## Drivers
Drivers are simpler components that provide low-level services without imposing
their own structure or flow. Examples:
- Database drivers
- File system access components
- External API clients

These interact with our application through **ports**:
- `TaskRepository` port for persistence operations
- `NotificationPort` for external notifications

Drivers typically only need two components:
- A port defined in the Application layer (like `TaskRepository(ABC)`)
- A concrete implementation in the Frameworks and Drivers layer
  (like `SqliteTaskRepository(TaskRepository)`)

Driver code example:
```Python
class SQLiteTaskRepository(TaskRepository):
    """Driver needs only basic interface implementation"""
    def save(self, task: Task) -> None:
        self.connection.execute(
            "INSERT INTO tasks (id, title) VALUES (?, ?)",
            (str(task.id), task.title)
            )
```

# Application Composition
**Application composition** is the systematic assembly of our system's components.
Three key aspects:
- Configuration Management
    - Manages environment-specific settings
    - Controls framework and driver selection
    - Maintains separation between settings and business logic
    - Enables different configurations for development, testing, and production
- Component Factories
    - Create properly configured implementations of interfaces
    - Manage dependency lifecycles
    - Handle initialization sequences
    - Maintain Clean Architecture's Dependency Rule during object creation
- Main Applicaiton Entry Point
    - Orchestrates startup sequence
    - Handles top-level error conditions
    - Maintains clean separation between startup and business operations
    - Serves as the composition root where dependencies are assembled

# Framework Adapters and "app dependency"
If you have a framework, like the "Click CLI" Python framework for creating
command-line interfaces, then your "ClickCli" adapter will pass all of the
interface/application/domain logic into it **as a dependency!**

In other words, we have applications inside applications!

```Python
class ClickCli:
    def __init__(self, app: Application): # this "app" is your inner logic!!!
        self.app = app

    def run(self) -> int:
        """Entry point for running Click CLI application"""
        try:
            while True:
                self._display_projects()

<...truncated code...>

    def _display_task_menu(self, task_id: str) -> None:
        """Display and handle task menu.
        Notice how "app" is called directly! Inner app is inside outer app."""
        result = self.app.task_controller.handle_get(task_id)
<...truncated code...>
```

# Framework Adapter and User Interaction
Framework adapters will manage user interactions as follows:
- Input Parsing
    - Validates and normalizes user input before processing
    - Provides clear feedback for invalid selections
    - Keeps input handling concerns at the framework boundary
- Command Routing
    - Maps users selections to appropriate handler methods
    - Maintains clean separation between input handling and business logic
    - Uses consistent patterns for different types of selection


# Database Adapters
Application Layer has a "TaskRepository" which ensures the business logic of
"keeping this thing persistent" is not infrastructure-dependent.
It has abstract methods for:
    - get
    - save
    - delete
    - find_by_project (return all tasks associated with a project id)
    - get_active_tasks (return all active tasks)
It also handles "domain-specific errors" like `TaskNotFoundError`

You can then implement this with:
- InMemoryTaskRepository which stores as a `Dict[UUID, Task]`
- FileTaskRepository which stores in a `tasks.json` file

# Config Class and Database Instantiation
The "Configuration management" aspect of our application is responsible for
selection and instantiation of our databases.

Here's his infrastructure/config.py:
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/main/Chapter_7/TodoApp/todo_app/infrastructure/config.py

**It seems the job of this class is essentially to grab environment variables!**
```Python
class Config:
    @classmethod
    def get_repository_type(cls) -> RepositoryType:
        # NOTE: os.getenv() is how to fetch an environment variable
        # You will need a separate system to load a .env file into memory
        repo_type_str = os.getenv(
            "TODO_REPOSITORY_TYPE",
            cls.DEFAULT_REPOSITORY_TYPE.value
        )
        try:
            return RepositoryType(repo_type_str.lower())
        except ValueError:
            raise ValueError(f"Invalid repository type: {repo_type_str}")
```

Then elsewhere we can do:
```Python
def create_repositories() -> Tuple[TaskRepository, ProjectRepository]:
    repo_type = Config.get_repository_type()
    if repo_type == RepositoryType.FILE:
        data_dir = Config.get_data_directory()
        task_repo = FileTaskRepository(data_dir)
        project_repo = FileProjectRepository(data_dir)
        project_repo.set_task_repository(task_repo)
        return task_repo, project_repo
    elif repo_type == RepositoryType.MEMORY:
        task_repo = InMemoryTaskRepository()
        project_repo = InMemoryTaskRepository()
        project_repo.set_task_repository(task_repo)
        return task_repo, project_repo
    else:
        raise ValueError(f"Invalid repository type: {repo_type_str}")
```

# External Applications
Here's an example of how to integrate with an external application via an
API key:
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_7/TodoApp/todo_app/infrastructure/notifications/sendgrid.py


# main.py and Application Bootstrapping
Note that OUTSIDE OF THE `TodoApp` MODULE ENTIRELY, lives the `main.py` that
is the actual entrypoint for the application!!!
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/main/Chapter_7/TodoApp/main.py

This `main.py` calls `create_application` which coordinates with configuration
management and component factories to assemble a fully-configured
`Application` class instance.

This `Application` class instance is in:
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_7/TodoApp/todo_app/infrastructure/configuration/container.py
`Application` lives in our Frameworks and Drivers layer, coordinating with
controllers in the Interface Adapters layer to provide framework adapters with
access to our core business logic.
**It holds all required application components as fields!**
It then creates all use_cases, then creates controllers with them!
For example, it creates:
- create_task_use_case
- complete_task_use_case
- get_task_use_case
- delete_task_use_case
- update_task_use_case
Then inits a `TaskController("insert use cases")` with them!!

Since use_cases and controllers are fundamental to our Application, they are
set up during `__post_init__`. However since Notifications, TaskPresenters,
ProjectPresenters, and Repositories (databases) are external to our Application,
we instead use a `create_application()` factory which takes the first three
as dependencies (then calls the "create_repositories()" function inside).
Basically, our Application class now only has dependencies on the inner layers.
The rest are dependency injection... (except the repositories? I'm confused)

`main.py` essentially:
- Creates our "application" named `app`
- Passes our `app` into the framework like:
```Python
cli = ClickCli(app)
return cli.run()
```
"This separation is significant: we could replace this CLI-specific main
with a web application entry point that uses the same `create_application`
factory but initializes a different framework adapter like FastAPI or
Flask instead of a ClickCLI."
