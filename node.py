from dataclasses import dataclass
from state import State

# Python dataclass for representing a node in the Search Tree:
@dataclass
class Node:
    state: State
    parent: "Node | None" = None
    action: str | None = None
    g: int = 0
    h: int = 0

    # We define "f(n) = g(n) + h(n)", used in A* search:
    @property
    def f(self):
        return self.g + self.h