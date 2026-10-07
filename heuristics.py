from state import State

# Manhattan Distance (TEST):
def manhattan(state: State, goal:State) -> int:
    return abs(state.x - goal.x) + abs(state.y - goal.y)

# Chebyshev Distance (TEST):
def chebyshev(state: State, goal: State) -> int:
    return max(abs(state.x - goal.x), abs(state.y - goal.y))

# All available heuristics:
HEURISTICS = {
    "manhattan": manhattan,
    "chebyshev": chebyshev
}