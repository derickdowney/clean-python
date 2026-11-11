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
