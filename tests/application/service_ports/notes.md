# Ports vs DTOs
DTOs are how our application "receives" API calls.

Ports are how our application "transmits" calls to external services.

Ports allow the Application Layer to specify EXACTLY what capabilities it needs
from external services without being coupled to specific implementations.
See application/service_ports/notifications.py for an example abtract class.
