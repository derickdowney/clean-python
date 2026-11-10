from dataclasses import dataclass


@dataclass(frozen=True)
class CompleteProjectRequest:
    """Data structure for project completion requests"""

    project_id: str  # From API (will be converted to UUID)
