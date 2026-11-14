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

# Managing Web Session Data
"Session data and form state present unique challenges for maintaining
Clean Architecture's boundaries."

Anti-pattern:
```Python
class Task:
    def complete(self, web_app_container):
        # Wrong: task shouldn't know about web sessions!
        self.completed_by = web_app_container.user.id
```

The correct pattern provided has nothing to do with the "completed_by"
anti-pattern above. The only thing that has to do with "session data" in the
correct pattern is that `flash(error.message, "error")` is a Flask function
that stores a temporary notification message in the user's session.
However it does capture the user's preference of "whether to show completed
projects in the list of all projects", but that's captured as a query parameter,
not specifically session data...
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_9/chapter_code_excerpts/10_flask_index_route.py

Interesting to note that it always grabs the "inner app logic" by doing the
`app = current_app.config["APP_CONTAINER"]`. I'm not sure what that is...

# Web Form Handling and Validation
A "validation" anti-pattern is to spread the validation logic across all
templates, controllers, and domain entities. Instead, we should have:
- Web Framework (Infrastructure Layer)
    - Endpoint extracts user's arguments from query params or post request body
    - Framework calls a `handle_` command on the `controller`, and forwards
      exact arguments as standard basic Python types (str, int, None)
    - Framework displays results from `interface.controller`
    - **No real validation! This just extracts needed args and forwards them!**
- Controller (Interface Layer)
    - Receives the handle request
    - Passes incoming args into an `application.DTO` Data Transfer Object.
      This converts the data from basic types to Domain types.
    - Calls the appropriate `application.use_case` with this DTO.
    - Returns the results from the `use_case.execute()`
    - **THIS CAPTURES EXCEPTIONS, BUT DOES NOT RAISE THEM**
    - **No real validation!** Although it wraps everything in a `ValueError`
      try-catch, because the DTO conversion process can return multiple
      kinds of value errors if the user's incoming args are invalid. If this
      "catch" is hit, then it presents the failure with a "VALIDATION_ERROR"
      style of presenter.
- DTO (Application Layer)
    - **THIS IS WHERE ARG VALIDATION HAPPENS!!!**
    - First, it stores the incoming args as fields.
        - Note that they're stored as their "basic primitive type" like strings
    - During `__post_init__` the incoming arguments are validated.
      It raises a ton of `ValueError` throughout this validation process!
      No other error is raised here! No business-rule errors
    - Then, it has the method named `to_execution_params` which converts the
      stored fields into the Domain types needed for use_case execution
    - **THIS RAISES MANY ValueError EXCEPTIONS!!!***
- Use Case (Application Layer)
    - Receives the DTO as an argument, and calls `to_execution_params` on it
      to receive actual args needed through this use_case function.
    - **THIS CAPTURES EXCEPTIONS BUT DOES NOT RAISE THEM!!!**
    - This orchestrates Domain Entities interaction with Service Ports and
      Repositories. **THE SERVICE PORTS AND REPOSITORIES CAN RAISE VALUE ERROR
      AND BUSINESS RULE EXCEPTIONS!!!**

I CAPTURED ALL OF THIS AS A PDF IN THE ROOT OF THIS PROJECT!
It is called: "validation_exception_handling_cheat_sheet.pdf"


## Immediate Client-Side Web Form Validation
In the example above, the web form content is not validated until it's submitted
to our server and run through our core logic.

However, we may want to give the user more instant "client-side" validation
so the app feels snappier and gives a better UX.

We can do this using something like the WTForms Python library. This library can
mirror domain validation rules in the "view" layer, enabling responsive UX
without duplicating validation logic.

The key here is that **view-layer validations must remain thin wrappers around
our core domain rules rather than introduce parallel validation logic!**

# Flask Factory
The Flask factory takes in configuration values, and also accepts an 
"app container." An "app container" is a specific instance of your inner app
logic, along with all of the external dependencies it needs (notifications,
repositories, etc.)

Example of flask factory: https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_9/chapter_code_excerpts/12_web_factory_method.py

# Entrypoint (App Container + Web Container)
NOTE:
    - "Web Container" = container for our web framework's application
    - "App Container" = container for all application logic below web framework

`web_main.py` acts as the overall application entrypoint.

It first creates the "application container" which contains all of our inner
logic plus dependencies.

It then creates the "Flask app" itself, referencing the application container.

The Flask app then creates the web container application, which uses the
"application container."

It says this setup "...enables runtime configuration of concrete implementations
through environment variables." p. 242
This means that you can changes your application's task repository from
"file" to "memory" just by editing your .env file!

Here's the entire `web_main.py`! 
```Python
def main():
    """Create and run the Flask web application."""
    app_container = create_application(
        notification_service=NotificationRecorder(),
        task_presenter=WebTaskPresenter(),
        project_presenter=WebProjectPresenter(),
    )

    flask_app = create_web_app(app_container)
    flask_app.run(debug=True)


if __name__ == "__main__":
    main()
```


Here's the environment config + script to run it:
https://github.com/PacktPublishing/Clean-Architecture-with-Python/blob/3459f4bcd6b7b63c5960e26720ffd05981b48736/Chapter_9/chapter_code_excerpts/17_run_web_app.sh.txt

