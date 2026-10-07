from state import State, Ori

# Displacements for each orientation:
DIRECTIONS = {
    Ori.NORTH: (-1, 0),
    Ori.NORTHEAST: (-1, 1),
    Ori.EAST: (0, 1),
    Ori.SOUTHEAST: (1, 1),
    Ori.SOUTH: (1, 0),
    Ori.SOUTHWEST: (1, -1),
    Ori.WEST: (0, -1),
    Ori.NORTHWEST: (-1, -1)
}

# Function to obtain all successors of a given state:
def get_successors(state, terrain):
    successors = []

    # We obtain the number of rows and columns from the already analyzed terrain:
    num_rows = len(terrain)
    num_cols = len(terrain[0])

    # First, we find the successor if we moved forward:
    dx, dy = DIRECTIONS[state.o] # X and Y displacement
    new_x = state.x + dx
    new_y = state.y + dy

    # We check that the movement is valid (if it remains inside the terrain):
    if 0 <= new_x < num_rows and 0 <= new_y < num_cols:
        new_state = State(new_x, new_y, state.o)

        # We compute the cost (which is the hardness of the destination cell):
        cost = terrain[new_x][new_y]

        successors.append((new_state, "MOVE", cost))

    # Secondly, we find the successor if we rotate 45 degrees clockwise:
    new_ori_clockwise = Ori((state.o.value + 1) % 8)
    new_state = State(state.x, state.y, new_ori_clockwise)

    # We add the succesor. The cost of a rotation is always 1:
    successors.append((new_state, "ROTATE_CW", 1))

    # Finally, we find the successor if we rotate 45 degrees counterclockwise:
    new_ori_cclockwise = Ori((state.o.value - 1) % 8)
    new_state = State(state.x, state.y, new_ori_cclockwise)

    # We add the succesor. The cost of a rotation is always 1:
    successors.append((new_state, "ROTATE_CCW", 1))

    return successors