from state import State, Ori

# Auxiliary function to parse a line with exactly "count" integers:
def parse_ints(line, count, description):
    values = line.split()

    if len(values) != count:
        raise ValueError(f"{description}: expected {count} values, found {len(values)} ('{line}')")

    try:
        return [int(v) for v in values]
    except ValueError:
        raise ValueError(f"{description}: all values must be integers ('{line}')")


# Auxiliary function to parse and check a "x y o" position line:
def parse_position(line, num_rows, num_cols, valid_oris, description):
    x, y, o = parse_ints(line, 3, description)

    # The position must be inside the terrain:
    if not (0 <= x < num_rows and 0 <= y < num_cols):
        raise ValueError(f"{description}: position ({x}, {y}) is outside the {num_rows}x{num_cols} map")

    # The orientation must be one of the allowed ones:
    if o not in valid_oris:
        raise ValueError(f"{description}: invalid orientation {o} (allowed: {min(valid_oris)}-{max(valid_oris)})")

    return State(x, y, Ori(o))


# Function to read the map given by a ".txt" file.
# It raises a "ValueError" if the file does not follow the expected format:
def read_map(file):
    with open(file, "r") as f:

        # The non-empty lines of the file are obtained:
        lines = []
        for line in f:
            if line.strip():
                lines.append(line.strip())

    if not lines:
        raise ValueError("The map file is empty")

    # We obtain the number of rows and columns from the first line:
    num_rows, num_cols = parse_ints(lines[0], 2, "Line 1 (map size)")

    if num_rows <= 0 or num_cols <= 0:
        raise ValueError(f"Line 1 (map size): the size must be positive ({num_rows}x{num_cols})")

    # The file must contain the size, the terrain rows and the two positions:
    if len(lines) != num_rows + 3:
        raise ValueError(
            f"Expected {num_rows + 3} non-empty lines (size, {num_rows} terrain rows, "
            f"initial and goal positions), found {len(lines)}"
        )

    # We obtain the terrain using the number of rows:
    terrain = []
    for i in range(1, num_rows + 1):
        row = parse_ints(lines[i], num_cols, f"Line {i + 1} (terrain row {i - 1})")

        # The hardness of each cell must be between 1 and 9:
        for value in row:
            if not 1 <= value <= 9:
                raise ValueError(f"Line {i + 1} (terrain row {i - 1}): hardness {value} is not between 1 and 9")

        terrain.append(row)

    # We obtain the initial state with the second to last row (any orientation except "ANY"):
    init_state = parse_position(lines[num_rows + 1], num_rows, num_cols, range(0, 8), "Initial position")

    # We obtain the goal state with the last row ("8" means that the orientation is irrelevant):
    goal_state = parse_position(lines[num_rows + 2], num_rows, num_cols, range(0, 9), "Goal position")

    return terrain, init_state, goal_state
