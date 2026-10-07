from collections import deque

from node import Node
from successors import get_successors
from common import is_goal, reconstruct_path

# Breadth-first search (graph search). The frontier is a FIFO queue and the goal
# test is done when a node is generated. It finds the solution with the fewest
# actions, which is not necessarily the cheapest one (costs are not uniform).
# It returns "(found, path, #E, #F)". If no solution is found, "path" goes
# from the initial node to the last examined node:
def bfs(terrain, init_state, goal_state):
    init_node = Node(state = init_state)

    # In case the initial state is already the goal:
    if is_goal(init_state, goal_state):
        return True, reconstruct_path(init_node), 0, 0

    # FIFO queue with the nodes to expand, and the set of their states:
    frontier = deque([init_node])
    frontier_states = {init_state}

    # Expanded states:
    visited = set()

    # Last examined node:
    current = init_node

    while frontier:
        current = frontier.popleft()
        frontier_states.discard(current.state)

        # We expand the current node:
        visited.add(current.state)

        for successor_state, action, cost in get_successors(current.state, terrain):
            # We ignore states already expanded or waiting in the frontier:
            if successor_state in visited or successor_state in frontier_states:
                continue

            successor_node = Node(
                state = successor_state,
                parent = current,
                action = action,
                g = current.g + cost
            )

            # Check if we reached the goal:
            if is_goal(successor_state, goal_state):
                return True, reconstruct_path(successor_node), len(visited), len(frontier)

            frontier.append(successor_node)
            frontier_states.add(successor_state)

    # In case no solution has been found:
    return False, reconstruct_path(current), len(visited), len(frontier)
