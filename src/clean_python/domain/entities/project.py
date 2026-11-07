from dataclasses import dataclass


@dataclass(eq=False)
class Project:
    name: str
    description: str = ""
