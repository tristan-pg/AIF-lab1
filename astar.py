import heapq

from node import Node
from successors import get_successors
from heuristics import *

# Auxiliary function to check if the current state is the goal:
def is_goal(state, goal):
    # In case the goal's orientation is irrelevant:
    if goal.o.value == 8:
        return state.x == goal.x and state.y == goal.y

    # In any other case, the orientation is checked as well:
    return state == goal


# Auxiliary function to rebuild the path:
def reconstruct_path(node):
    path = []

    # All the previous nodes are added:
    while node is not None:
        path.append(node)
        node = node.parent

    path.reverse()
    return path


def astar(terrain, init_state, goal_state, heuristic):
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

    while frontier:
        _, _, current = heapq.heappop(frontier)

        # We ignore obsolete entries in the priority queue:
        if frontier_nodes.get(current.state) is not current:
            continue

        # We remove the current node from the frontier:
        del frontier_nodes[current.state]

        # Check if we reached the goal:
        if is_goal(current.state, goal_state):
            return(reconstruct_path(current), visited_count, len(frontier_nodes))

        # Otherwise, we expand the current node:
        visited.add(current.state)
        visited_count += 1

        # Generate the successors:
        for successor_state, action, cost in get_successors(current.state, terrain):
            # We ignore previously expanded states:
            if successor_state in visited:
                continue

            new_g = current.g + cost

            # If this is a better path to the successor:
            if(successor_state not in best_g_score or new_g < best_g_score[successor_state]):
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

    # In case no solution has been found:
    return None, visited_count, len(frontier_nodes)