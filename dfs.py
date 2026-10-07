from node import Node
from successors import get_successors
from astar import is_goal, reconstruct_path

# Depth-first search (graph search). The frontier is a LIFO stack and the goal
# test is done when a node is selected for expansion. The visited set avoids
# cycles (e.g. rotating forever in place), so it is complete in our finite
# state space, but it is not optimal:
def dfs(terrain, init_state, goal_state):
    init_node = Node(state = init_state)

    # LIFO stack with the nodes to expand, and the set of their states:
    frontier = [init_node]
    frontier_states = {init_state}

    # Expanded states:
    visited = set()

    while frontier:
        current = frontier.pop()
        frontier_states.discard(current.state)

        # Check if we reached the goal:
        if is_goal(current.state, goal_state):
            return reconstruct_path(current), len(visited), len(frontier)

        # Otherwise, we expand the current node:
        visited.add(current.state)

        # Successors are pushed in reverse order so that the first one generated
        # (MOVE) is the first one to be expanded:
        for successor_state, action, cost in reversed(get_successors(current.state, terrain)):
            # We ignore states already expanded or waiting in the frontier:
            if successor_state in visited or successor_state in frontier_states:
                continue

            successor_node = Node(
                state = successor_state,
                parent = current,
                action = action,
                g = current.g + cost
            )

            frontier.append(successor_node)
            frontier_states.add(successor_state)

    # In case no solution has been found:
    return None, len(visited), len(frontier)
