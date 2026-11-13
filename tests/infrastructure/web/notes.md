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
|   |-web.py        // Web UI presenters
|-web_main.py       // Script to start web app
