import sys

from map_reader import read_map
from astar import astar
from bfs import bfs
from dfs import dfs
from heuristics import *

# Blind search algorithms (they do not use a heuristic):
BLIND_ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs
}

def main():

    # We check the number of arguments:
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python main.py <map_file> <algorithm> [heuristic]")
        return

    map_file = sys.argv[1]
    algorithm = sys.argv[2].lower()

    # We first read the map:
    try:
        terrain, init_state, goal_state = read_map(map_file)
    except (OSError, ValueError) as error:
        print(f"Error reading the map '{map_file}': {error}")
        return

    # We select the algorithm and run it:
    if algorithm == "astar":

        # A* requires a heuristic:
        if len(sys.argv) != 4:
            print("A* requires a heuristic")
            print("Available heuristics:",", ".join(HEURISTICS))
            return

        heuristic_name = sys.argv[3].lower()

        # In case the heuristic's name is not found:
        if heuristic_name not in HEURISTICS:
            print (f"Unknown heuristic: {heuristic_name}. ")
            print("Available heuristics:",", ".join(HEURISTICS))
            return

        heuristic = HEURISTICS[heuristic_name]

        # We run the algorithm:
        found, path, explored_count, frontier_count = astar(
            terrain,
            init_state,
            goal_state,
            heuristic
        )

    elif algorithm in BLIND_ALGORITHMS:

        # We run the algorithm:
        found, path, explored_count, frontier_count = BLIND_ALGORITHMS[algorithm](
            terrain,
            init_state,
            goal_state
        )

    else:
        print(f"Unknown algorithm: {algorithm}")
        print("Available algorithms: astar,", ", ".join(BLIND_ALGORITHMS))
        return
    
    # In case no solution has been found, the path to the last examined node is shown:
    if not found:
        print("No solution found. Path from the initial node to the last examined node:")

    last_label = "(final node)" if found else "(last examined node)"

    for depth, node in enumerate(path):
        # Each node is preceded by the operator that generated it:
        if depth > 0:
            print(f"Operator {depth}: {node.action}")

        if depth == 0:
            label = " (starting node)"
        elif depth == len(path) - 1:
            label = f" {last_label}"
        else:
            label = ""

        # Blind search nodes are shown as "(d, g(n), op, S)" and A* nodes as "(d, g(n), op, h(n), S)":
        if algorithm in BLIND_ALGORITHMS:
            print(f"Node {depth}{label}: ({depth}, {node.g}, {node.action}, {node.state})")
        else:
            print(f"Node {depth}{label}: ({depth}, {node.g}, {node.action}, {node.h}, {node.state})")

    print()
    print(f"Total number of items in explored list: {explored_count}")
    print(f"Total number of items in frontier: {frontier_count}")


if __name__ == "__main__":
    main()