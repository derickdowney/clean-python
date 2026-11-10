# Ports vs DTOs
DTOs are how our application "receives" API calls.

Ports are how our application "transmits" calls to external services.

Ports allow the Application Layer to specify EXACTLY what capabilities it needs
from external services without being coupled to specific implementations.
See application/service_ports/notifications.py for an example abtract class.

# Optional Services
You can easily make some services "required" while others are "optional."
See TaskManagementUseCase in application.use_cases.task_use_cases

# Service Adapters
You can easily adapt to service changes if you:
- Capture the external service within a standalone "Service" class
- Create an adapter which requires the "Service" class as a dependency

This way, if the external service changes, the "adapter" class remains the same.
All you'd have to do is initialize the adapter with a different Service class,
and the service calls will remain the same.
