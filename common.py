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


# Auxiliary function to show a node as "(d, g(n), op, S)", or as
# "(d, g(n), op, h(n), S)" for informed search:
def format_node(node, show_h = False):
    depth = len(reconstruct_path(node)) - 1

    if show_h:
        return f"({depth}, {node.g}, {node.action}, {node.h}, {node.state})"

    return f"({depth}, {node.g}, {node.action}, {node.state})"
