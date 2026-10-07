from state import Ori

# Auxiliary function to check if the current state is the goal:
def is_goal(state, goal):
    # In case the goal's orientation is irrelevant:
    if goal.o == Ori.ANY:
        return state.x == goal.x and state.y == goal.y

    # In any other case, the orientation is checked as well:
    return state == goal


# Auxiliary function to rebuild the path from the initial node to the given node:
def reconstruct_path(node):
    path = []

    # All the previous nodes are added:
    while node is not None:
        path.append(node)
        node = node.parent

    path.reverse()
    return path
