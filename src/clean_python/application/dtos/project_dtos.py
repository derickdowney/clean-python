from dataclasses import dataclass

from clean_python.domain.exceptions import ValidationError


@dataclass(frozen=True)
class CompleteProjectRequest:
    """Data structure for project completion requests"""

    project_id: str  # From API (will be converted to UUID)
    completion_notes: str | None = None

    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.project_id.strip():
            raise ValidationError("Project ID is required")
