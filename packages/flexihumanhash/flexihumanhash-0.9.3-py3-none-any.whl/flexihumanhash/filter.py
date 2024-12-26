from __future__ import annotations
from typing import Any

registry: dict[str, JingaFilter]

class JingaFilter:
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, old_val: str | int, *args: Any) -> str:
        return "bob"

    def register(self, name: str, filter: JingaFilter) -> None:
        registry[name] 