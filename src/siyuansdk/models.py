from dataclasses import dataclass


@dataclass
class Notebook:
    id: str
    name: str
    icon: str
    sort: int
    close: bool
