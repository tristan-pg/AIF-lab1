#!/usr/bin/env bash
# Usage: ./run.sh <map_file> <bfs|dfs|astar> [heuristic]
#        ./run.sh --experiments [seed]
# Requires only Python 3 (no external dependencies).
cd "$(dirname "$0")"
if [ "$1" = "--experiments" ]; then
    shift
    exec python3 experiments.py "$@"
fi
exec python3 main.py "$@"
