from dataclasses import dataclass
from enum import Enum

# Enumeration for representing different orientations:
class Ori(Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
    ANY = 8

# Python dataclass for representing a state:
@dataclass(frozen = True)
class State:
    x: int  # X Axis
    y: int  # Y Axis
    o: Ori  # Orientation