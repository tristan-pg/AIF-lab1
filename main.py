import sys

from map_reader import read_map
from astar import astar
from heuristics import *

def main():

    # We check the number of arguments:
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python main.py <map_file> <algorithm> [heuristic]")
        return

    map_file = sys.argv[1]
    algorithm = sys.argv[2].lower()

    # We first read the map:
    terrain, init_state, goal_state = read_map(map_file)

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
        path, explored_count, frontier_count = astar(
            terrain,
            init_state,
            goal_state,
            heuristic
        )

    else:
        print(f"Unknown algorithm: {algorithm}")
        print("Available algorithms: astar")
        return
    
    # In case no solution has been found:
    if path is None:
        print("No solution found.")
        print(f"#E: {explored_count}")
        print(f"#F: {frontier_count}")
        return

    # In another case:
    print("Solution found:")
    print()

    for depth, node in enumerate(path):
        print(
            f"({depth}, {node.g}, {node.action}, "
            f"{node.h}, {node.state})"
        )

    print()
    print(f"#E: {explored_count}")
    print(f"#F: {frontier_count}")


if __name__ == "__main__":
    main()