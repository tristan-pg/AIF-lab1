from state import State

# We obtain the following heuristic by relaxing the problem, by ignoring
# the cost of turning around. This also corresponds to the Chebyshev distance:
def no_turning_cost(state: State, goal: State):
    return max(
        abs(state.x - goal.x),
        abs(state.y - goal.y))

# All available heuristics:
HEURISTICS = {
    "no_turning_cost": no_turning_cost
}