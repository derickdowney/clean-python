# Interface Adapter Layer
This layer serves as the translator between our application's core and
external concerns. It converts data between formats convenient for
external agencies and those expected by our use cases.

It acts as a translator between our application's core and external details
such as a web framework or a command-line interface.

Just as an English-Spanish translator must be fluent in both languages, so must
the Interface Adapter layer understand the precise language of the application
core and the external interfaces.

It sits between the "Application layer" and "external interfaces."

Note: External services don't always require an adapter. For example, if you
have a `TaskRepository(ABC)` defined in the Application Layer with a clear
`get()` abstract method, then that might be enough for a
`SqliteTaskRepository(TaskRepository)` implementation directly in Infrastructure
layer! The key question for knowing when an adapter is needed is:
    *Does this interaction need format conversion between layers?*

# Controllers vs Presenters vs View Models
Controllers:
- Handle inbound data flow from user interfaces to application
- Serve as "entry points" for external requests into our system
    - FastAPI will ultimately interact with the controller!!!
- One controller should do all related usecases. For example:
    - TaskController would handle `task_create_use_case`,
      `task_complete_use_case`, `task_set_priority_use_case`, and so on.
- Since controllers are at boundaries, they always return a success/error RESULT
- Steps:
    - Inits with "Use Case" dependencies and "Presenter" dependencies
        - This is dependency injection
    - Does a "handle_xxx_use_case" method call
    - In method, converts external input into UseCase request format
    - In method, calls `result = self.xxx_use_case.execute(request)`
    - Then does:
```Python
if result.is_success:
    view_model = self.presenter.present_task(result.value)
    return OperationResult.succeed(view_model)

error_view_model = self.presenter.present_error(
    result.error.message,
    str(result.error.code.name)
)
return OperationResult.fail(error_view_model.message, error_view_model.code)
```

Presenters:
- Handle outbound data flow from application to user interfaces
- Transform use case results into formats suitable for external consumption

View models
- Data carriers between presenters and views
- Contains only primitive types and simple data structures

# Data Transformations in Application Layer vs Interface Layer
Application layer data transformations:
- Transforms between domain entities and use case formats
- Focuses on business rule coordination
- Works with domain-specific types and structures

Interface adapters layer data transformations:
- Transforms between use case formats and external interface needs
- Focuses on external interface coordination
- Works with interface-specific formats and primitive types

# Data Transformation Flow
As data moves through our architectural boundaries, it transforms each time:
1. External input validation and conversion
2. Use case execution with domain types
3. Success case transformation to view model
4. Error case handling and formatting
5. Validation error handling

# Interaction Flow
1. External requests flow through controllers
2. Controllers coordinate with use cases
3. Use cases return results through defined interfaces
4. Presenters format results into view models
5. Views consume the formatted data

# Interface Adapters Design Principles
- Dependency Rule
    - Outer layers can only depend upon inner layers as explicit arguments
- Single Responsibility Prinicipal
    - Each adapter handles one type of transformation
    - TaskController focuses solely on validating/converting task-related input
    - TaskPresenter handles only the formatting of task data for display
- Interface Segregation Priniciple
    - Create small purpose-specific interfaces that serve distinct client needs
    - Don't create large monolithic interfaces
    - Instead of a large `TaskOperations` interface, do:
        - One for task creation
        - One for task completion
        - One for task queries

# OperationResult Class
- Provides a standardized way to handle both success and failure cases
- It uses `OperationResult[T]` generic which allows you to instantiate like:
    - `OperationResult[User]`
    - `OperationResult[TaskViewModel]`
    - `OperationResult[Task]`
- This generic makes it so that the class with either return:
    - ErrorViewModel (because that field is static across all instances)
    - or, whatever `[T]` class you specify during instantiation
- These generics are like passing in an `Object` argument, except:
    - Using an `Object` arg relies on runtime polymorphism
    - Generics are compile-time type safety
    - Object arg loses type safety and autocomplete; Generics retain them!
    - If you do `[User]`, then you can call a field on that user later!
      Whereas if you use Object polymorphism, Object won't have that field!

