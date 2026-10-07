import sys

from map_reader import read_map
from astar import astar
from bfs import bfs
from dfs import dfs
from heuristics import *
from common import format_node

# Blind search algorithms (they do not use a heuristic):
BLIND_ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs
}

def main():

    # The "-v" (or "--verbose") option can be given in any position:
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ("-v", "--verbose")]

    # We check the number of arguments:
    if len(args) < 2 or len(args) > 3:
        print("Usage: python main.py <map_file> <algorithm> [heuristic] [-v]")
        return

    map_file = args[0]
    algorithm = args[1].lower()

    # In verbose mode, the search process is printed step by step:
    log = print if verbose else None

    # We first read the map:
    try:
        terrain, init_state, goal_state = read_map(map_file)
    except (OSError, ValueError) as error:
        print(f"Error reading the map '{map_file}': {error}")
        return

    # We select the algorithm and run it:
    if algorithm == "astar":

        # A* requires a heuristic:
        if len(args) != 3:
            print("A* requires a heuristic")
            print("Available heuristics:",", ".join(HEURISTICS))
            return

        heuristic_name = args[2].lower()

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
            heuristic,
            log
        )

    elif algorithm in BLIND_ALGORITHMS:

        # We run the algorithm:
        found, path, explored_count, frontier_count = BLIND_ALGORITHMS[algorithm](
            terrain,
            init_state,
            goal_state,
            log
        )

    else:
        print(f"Unknown algorithm: {algorithm}")
        print("Available algorithms: astar,", ", ".join(BLIND_ALGORITHMS))
        return
    
    # The trace is separated from the final path:
    if verbose:
        print()

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
        print(f"Node {depth}{label}: {format_node(node, algorithm not in BLIND_ALGORITHMS)}")

    print()
    print(f"Total number of items in explored list: {explored_count}")
    print(f"Total number of items in frontier: {frontier_count}")


if __name__ == "__main__":
    main()