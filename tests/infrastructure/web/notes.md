# Adding a Web UI
When you use Clean Architecture, adding a web interface becomes a 
"purely additive exercise. No refactoring of existing components is required."

He'll be using Flask for this TodoApp.

# Folder structure
todo_app
|-application
|-domain
|-infrastructure
| |-web
|   |-app.py        // Flask app setup
|   |-routes.py     // Route requests to Controllers
|   |-templates
|     |-            // Additional templates
|     |-index.html  // landing page for web app
|-interfaces
| |-presenters
|   |-web.py        // Web UI presenters, which are framework independent!!!
|-web_main.py       // Script to start web app

# Interfaces vs Infrastructure
"Interface layer" is where web presenters format data for web display, creating
HTML-friendly strings and structuring data for templates. But **they remain
completely unaware of Flask or any specific web framework!!**

All "framework specific" code lives in "infrastructure/web" directory!

Now:
- CLI's "Click command handler" routes to core "Task Controller"
- Flasks's route handler also routes to same core "Task Controller"

There's an awesome graphic for this....

```
          CLI                    Shared Core               Web Interface

[Command line input     ]                                  [ HTTP Request       ]
            |                                                       |
[Click command handler  ] --- [Task controller      ] ---- [Flask route handler ]
            |                           |                           |
[CLI presenter          ]     [Create task use case ]      [Web presenter       ]
            |                           |                           |
[Console output         ]     [Task entity          ]      [HTML template       ]
```

# Application Factory
The `infrastructure/configuration/container.py` is where the "application"
container lives, and allows you to inject whatever custom dependencies
your specific instance of the application needs.

```Python
# todo_app/infrastructure/configuration/container.py
@dataclass
class Application:
    """Container which wires together all components."""

    task_repository: TaskRepository
    project_repository: ProjectRepository
    notification_service: NotificationPort
    task_presenter: TaskPresenter
    project_presenter: ProjectPresenter
```

Meanwhile the factory method **constructs core infrastructure internally
(the repositories)**. This means that your outer application can declare
dependencies for things relevant to it (notification, presenters), but it
cannot declare the type of repository it uses. Therefore all instances of
your app use the same exact repository!
```Python
# todo_app/infrastructure/configuration/container.py
def create_application(
    notification_service: NotificationPort,
    task_presenter: TaskPresenter,
    project_presenter: ProjectPresenter,
) -> "Application":
    """Factory function for the Application container."""
    task_repository, project_repository = create_repositories()

    return Application(
        task_repository=task_repository,
        project_repository=project_repository,
        notification_service=notification_service,
        task_presenter=task_presenter,
        project_presenter=project_presenter,
    )
```


Finally, this means your CLI application can do something like:
```Python
# cli_main.py
def main() -> int:
    """Main entry point for the CLI application."""
    app = create_application(
        notification_service=NotificationRecorder(),
        task_presenter=CliTaskPresenter(),
        project_presenter=CliProjectPresenter(),
    )
    cli = ClickCli(app)
    return cli.run()
```

# Controllers Must Remain Framework Agnostic
Do NOT reference anything to do with "Click" or "Flask" in `TaskController`
It should always return an "operation result" instead.
And it should always rely on the abstract `presenter` interface.
And it should only accept generic arg types like "strings".
So it should look like:
```Python
if result.is_success:
    view_model = self.presenter.present_task(result.value)
    return OperationResult.succeed(view_model)

error_vm = self.presenter.present_error(
    result.error.message, str(result.error.code.name)
)
return OperationResult.fail(error_vm.message, error_vm.code)
```

# Web-Specific Presenters
Our WebTaskPresenter can take the data from a TaskResponse and format it
exactly as our Web UI needs it.

```Python
class WebTaskPresenter(TaskPresenter):
    
    def present_task(self, task_response: TaskResponse) -> TaskViewModel:
        return TaskViewModel(
            id=task_response.id,
            title=task_response.title,
            ...,
            completion_info=self._format_completion_info(
                task_response.completion_date,
                task_response.completion_notes
            ),
        )
```

The `_format_completion_info` function is where timezone handling happens.

## Flask Templates
Flask templates can then take in this "TaskViewModel", parse the data
from them, and inject them into the exact HTML that we want!
"ViewModels" control the data formatting, and Templates control the styling.

## Web Presenter Unit Tests
Clean Architecture's "presenter" pattern allows us to verify formatting logic
without any complex web setup! No need for Flask test clients, mock databases,
or HTML parsing!

See example of web presenter unit tests here:
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_9/chapter_code_excerpts/08_web_presenter_tests.py

## Presenters vs template-based formatting
Modern web frameworks embed formatting directly into templates, but this blurs
the boundary between presentation decisions and display structure.
Clean Architecture says **treat templates purely as display structure**!!!

Not all frameworks will have "formatting helpers."
Be consistent and do all the formatting for all layers in the Presenters class.

# Managing Web-Specific State
# LEFT OFF HERE!!!!! p. 234
