from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Entity:
    # Automatically generaete a unique UUID for the 'id' field;
    # excluded from the __init__ method
    id: UUID = field(default_factory=uuid4, init=False)
