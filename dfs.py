from node import Node
from successors import get_successors
from common import is_goal, reconstruct_path, format_node

# Depth-first search (graph search). The frontier is a LIFO stack and the goal
# test is done when a node is selected for expansion. The visited set avoids
# cycles (e.g. rotating forever in place), so it is complete in our finite
# state space, but it is not optimal.
# It returns "(found, path, #E, #F)". If no solution is found, "path" goes
# from the initial node to the last examined node.
# If "log" is given (e.g. "print"), the search process is traced step by step.
def dfs(terrain, init_state, goal_state, log = None):
    init_node = Node(state = init_state)

    # LIFO stack with the nodes to expand, and the set of their states:
    frontier = [init_node]
    frontier_states = {init_state}

    # Expanded states:
    visited = set()

    # Last examined node:
    current = init_node

    while frontier:
        current = frontier.pop()
        frontier_states.discard(current.state)

        # Check if we reached the goal:
        if is_goal(current.state, goal_state):
            if log:
                log(f"Goal reached: {format_node(current)}")
            return True, reconstruct_path(current), len(visited), len(frontier)

        # Otherwise, we expand the current node:
        visited.add(current.state)
        added = 0

        if log:
            log(f"[{len(visited)}] Expanding {format_node(current)} | frontier: {len(frontier)}")

        # Successors are pushed in reverse order so that the first one generated
        # (MOVE) is the first one to be expanded:
        for successor_state, action, cost in reversed(get_successors(current.state, terrain)):
            # We ignore states already expanded or waiting in the frontier:
            if successor_state in visited or successor_state in frontier_states:
                if log:
                    log(f"      - {action} -> {successor_state} repeated, ignored")
                continue

            successor_node = Node(
                state = successor_state,
                parent = current,
                action = action,
                g = current.g + cost
            )

            frontier.append(successor_node)
            frontier_states.add(successor_state)
            added += 1

            if log:
                log(f"      + {format_node(successor_node)}")

        # If no new successor was added, the search goes back to the last pending node:
        if log and added == 0:
            log("      Dead end, backtracking")

    # In case no solution has been found:
    return False, reconstruct_path(current), len(visited), len(frontier)
