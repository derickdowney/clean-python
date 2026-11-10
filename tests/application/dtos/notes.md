# Data Transfer Objects (DTOs)
DTOs are "models" of structured data that transfer state between
architectural boundaries.

They are essentially saying, "If you want to talk to the domain layer,
you must provide the input (request) in this format, and you can expect the
output (response) in this other format."

By working with DTOs, we ensure that **application use cases can work purely
with domain objects while input and output are automatically adapted to
external needs!!!**

# Request Models
Request models establish a clear boundary between outer and inner layers,
validate input received from outer layers, and convert those API-friendly
formats (like string IDs) into proper domain types (like UUIDs).

This means that, by the time data reaches our application use cases, we know
they have been validated and transformed into the proper format. So things like
"HTTP request conversion validation" is totally removed from business domain
logic!

Sam Keen uses a frozen @dataclass as his request model class,
then the "__post_init__()" to validate the input,
then a "to_execution_params()" to convert the outer input into inner input.

# Response Models
Response models transform domain objects into structures suitable for
external consumption. They control what data is exposed and how it is formatted.

They provide a consistent serialization point for all external interfaces.

Sam Keen does this with a single @classmethod named `from_entity()`
This is essentially a "special constructor" which creates an instance of the
CompleteProjectResponse object with API-safe content.
