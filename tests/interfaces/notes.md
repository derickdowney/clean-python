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

# Controllers vs Presenters vs View Models
Controllers:
- Handle inbound data flow from user interfaces to application
- Serve as "entry points" for external requests into our system

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


