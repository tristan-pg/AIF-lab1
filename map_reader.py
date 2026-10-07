from state import State, Ori

# Function to read the map given by a ".txt" file:
def read_map(file):
    with open(file, "r") as f:

        # The lines of the file are obtained:
        lines = []
        for line in f:
            lines.append(line.strip())

        # We obtain the number of rows and columns from the first line:
        num_rows, num_cols = map(int, lines[0].split())

        # We obtain the terrain using the number of rows:
        terrain = []
        for i in range(1, num_rows + 1):
            row = list(map(int, lines[i].split()))
            terrain.append(row)

        # We obtain the initial state with the second to last row:
        xi, yi, oi = map(int, lines[num_rows + 1].split())
        init_state = State(xi, yi, Ori(oi))

        # We obtain the goal state with the last row:
        xg, yg, og = map(int, lines[num_rows + 2].split())
        goal_state = State(xg, yg, Ori(og))

        return terrain, init_state, goal_state