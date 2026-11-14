# Logging and Observability
Logging can be very difficult in tightly-coupled systems.
Clean Architecture makes it easy to log the transitions between each boundary:
- Web interface incoming requests and their transformations
- Use case business operations and their outcomes
- Domain entity state changes and business rule applications
- Infrastructure component resource utilization and external interactions

# Operation Lifecycle and Logging
Example lifecycle of a "complete task" operation plus logging/monitoring.
The benefit here is that, when a user reports intermittent task completion
failures, we can clearly follow the operation and identify where it went wrong!
Each layer tracks what it knows best.

- Web/CLI Request
    - Monitor: Request Receipt
    - Forwards request to complete task to controller
- Controller
    - Monitor: Input validation
    - Invokes task completion use case
- Use Case
    - Monitor: Task state change
    - Changes task state in Domain entities
- Domain
    - Monitor: Business rules
    - Persists task state in repository
- Repository
    - Persists task state
    - Returns persist result
- Domain
    - Returns result
- Use Case
    - Returns result
- Controller
    - Returns result
- Web/CLI Request
    - Returns result


# Web Framework Logging
Modern web frameworks often provide their own logging infrastructure, but
**we must not couple our business operations with framework-specific logging!**
We can work with them, but we must keep our core logic framework-indepedent.


# Framework Agnostic Logging
Below is an example of how to implement a framework-agnostic logger.

It allows us to:
- Keep use cases unaware of logging implementation details
- Document business operations using natural logging statements
- Change logging infrastructure without modifying business logic
- Keep framework-specific logging at system edges

```Python
# todo_app/application/use_cases/task_use_cases.py
import logging
logger = logging.getLogger(__name__)

@dataclass
class CreateTaskUseCase:
    task_repository: TaskRepository
    project_repository: ProjectRepository

    def execute(self, request: CreateTaskRequest) -> Result:
        try:
            logger.info(
                "Creating new task",
                extra={"context": {
                    "title": request.title,
                    "project_id": request.project_id
                }},
                )
            # ...implementation continues...
```

# LEFT OFF ON PAGE 250
