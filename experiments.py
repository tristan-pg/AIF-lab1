import random
import sys

from state import State, Ori
from astar import astar
from bfs import bfs
from dfs import dfs
from heuristics import HEURISTICS

# Section 3.4.2: mean d, g, #E and #F over 5 random NxN maps for each size:
SIZES = (3, 5, 7, 9)
RUNS = 5

# All the methods to compare, as "name: function(terrain, init_state, goal_state)":
METHODS = {"Breadth-first": bfs, "Depth-first": dfs}
for name, heuristic in HEURISTICS.items():
    METHODS[f"A* ({name})"] = lambda t, i, g, h = heuristic: astar(t, i, g, h)


# Function to generate a random NxN map, from (0, 0) facing North to (N-1, N-1) in any orientation:
def random_problem(n, rng):
    terrain = [[rng.randint(1, 9) for _ in range(n)] for _ in range(n)]
    return terrain, State(0, 0, Ori.NORTH), State(n - 1, n - 1, Ori.ANY)


def main():
    # The seed can be given as an argument to reproduce the tables:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    rng = random.Random(seed)

    for n in SIZES:
        problems = [random_problem(n, rng) for _ in range(RUNS)]

        print(f"\nTable: performance of search methods on {n}x{n} maps (mean of {RUNS})")
        print(f"| {'Method':<16} | {'d':>6} | {'g':>6} | {'#E':>6} | {'#F':>6} |")
        print(f"|{'-' * 18}|{'-' * 8}|{'-' * 8}|{'-' * 8}|{'-' * 8}|")

        for name, method in METHODS.items():
            results = [method(*problem) for problem in problems]
            d = sum(len(path) - 1 for _, path, _, _ in results) / RUNS
            g = sum(path[-1].g for _, path, _, _ in results) / RUNS
            e = sum(explored for _, _, explored, _ in results) / RUNS
            f = sum(frontier for _, _, _, frontier in results) / RUNS
            print(f"| {name:<16} | {d:6.1f} | {g:6.1f} | {e:6.1f} | {f:6.1f} |")


if __name__ == "__main__":
    main()
