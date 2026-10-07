import heapq

from node import Node
from successors import get_successors
from common import is_goal, reconstruct_path, format_node
from heuristics import *

# A* search (graph search), ordered by "f(n) = g(n) + h(n)".
# It returns "(found, path, #E, #F)". If no solution is found, "path" goes
# from the initial node to the last examined node.
# If "log" is given (e.g. "print"), the search process is traced step by step.
def astar(terrain, init_state, goal_state, heuristic, log = None):
    init_node = Node(
        state = init_state,
        g = 0,
        h = heuristic(init_state, goal_state)
    )

    # Prioirty queue "(f, ins_order, node)". It will be ordered by "f":
    frontier = []
    ins_order = 0 # The insertion order will be used as a tie-breaker

    heapq.heappush(frontier, (init_node.f, ins_order, init_node))

    # Best known g-score for each state:
    best_g_score = {init_state: 0}

    # Nodes currently in the frontier:
    frontier_nodes = {init_state: init_node}

    # Visited nodes and their number:
    visited = set()
    visited_count = 0

    # Last examined node (obsolete entries do not count):
    last_examined = init_node

    while frontier:
        _, _, current = heapq.heappop(frontier)

        # We ignore obsolete entries in the priority queue:
        if frontier_nodes.get(current.state) is not current:
            continue

        # We remove the current node from the frontier:
        del frontier_nodes[current.state]
        last_examined = current

        # Check if we reached the goal:
        if is_goal(current.state, goal_state):
            if log:
                log(f"Goal reached: {format_node(current, True)}")
            return True, reconstruct_path(current), visited_count, len(frontier_nodes)

        # Otherwise, we expand the current node:
        visited.add(current.state)
        visited_count += 1

        if log:
            log(f"[{visited_count}] Expanding {format_node(current, True)} "
                f"| f = {current.f} | frontier: {len(frontier_nodes)}")

        # Generate the successors:
        for successor_state, action, cost in get_successors(current.state, terrain):
            # We ignore previously expanded states:
            if successor_state in visited:
                if log:
                    log(f"      - {action} -> {successor_state} already explored, ignored")
                continue

            new_g = current.g + cost

            # If this is a better path to the successor:
            if(successor_state not in best_g_score or new_g < best_g_score[successor_state]):
                improved = successor_state in best_g_score
                successor_h = heuristic(successor_state, goal_state)

                # We obtain the successor node:
                successor_node = Node(
                    state = successor_state,
                    parent = current,
                    action = action,
                    g = new_g,
                    h = successor_h
                )

                best_g_score[successor_state] = new_g

                ins_order += 1

                heapq.heappush(frontier, (successor_node.f, ins_order, successor_node))
                frontier_nodes[successor_state] = successor_node

                if log:
                    note = " (better path to a state in the frontier)" if improved else ""
                    log(f"      + {format_node(successor_node, True)}{note}")

            elif log:
                log(f"      - {action} -> {successor_state} with g = {new_g}, "
                    f"not better than {best_g_score[successor_state]}, ignored")

    # In case no solution has been found:
    return False, reconstruct_path(last_examined), visited_count, len(frontier_nodes)