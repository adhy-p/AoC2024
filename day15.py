from copy import deepcopy

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)
DIRS = [RIGHT, DOWN, LEFT, UP]

sym_to_dir = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}


def get_input() -> tuple[list[list[str]], list[str]]:
    with open("day15.txt", "r") as f:
        maze, instructions = f.read().split("\n\n")
        maze = [list(line) for line in maze.splitlines()]
        return maze, instructions


def push_boxes(
    maze: list[list[str]],
    coord: tuple[int, int],
    direction: tuple[int, int],
) -> bool:
    def is_within_bounds(coord: tuple[int, int]) -> bool:
        return (
            coord[0] >= 0
            and coord[0] < len(maze)
            and coord[1] >= 0
            and coord[1] < len(maze[1])
        )

    row, col = coord
    prev_row, prev_col = row - direction[0], col - direction[1]
    next_row, next_col = row + direction[0], col + direction[1]

    if not is_within_bounds(coord) or maze[row][col] == "#":
        return False

    if maze[row][col] == ".":
        maze[prev_row][prev_col], maze[row][col] = (
            maze[row][col],
            maze[prev_row][prev_col],
        )
        return True
    can_move = push_boxes(maze, (next_row, next_col), direction)
    if can_move:
        maze[prev_row][prev_col], maze[row][col] = (
            maze[row][col],
            maze[prev_row][prev_col],
        )
        return True
    return False


def find_robot(maze: list[list[str]]) -> tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "@":
                return (i, j)
    assert False


def part1(maze: list[list[str]], instructions: str) -> int:
    r, c = find_robot(maze)

    for i in instructions:
        if i == "\n":
            continue
        # print((r, c), i)
        direction = sym_to_dir[i]
        new_r, new_c = (r + direction[0], c + direction[1])
        push_succeeded = push_boxes(maze, (new_r, new_c), direction)
        if push_succeeded:
            r, c = new_r, new_c
        # for row in maze:
        #     print("".join(row))

    ans = 0
    for ridx, row in enumerate(maze):
        for cidx, tile in enumerate(row):
            if tile == "O":
                ans += 100 * ridx + cidx
    return ans


def transform_maze(maze: list[list[str]]) -> list[list[str]]:
    new_maze = []
    for row in maze:
        new_row = []
        for char in row:
            match char:
                case "#":
                    new_row.append("#")
                    new_row.append("#")
                case "O":
                    new_row.append("[")
                    new_row.append("]")
                case ".":
                    new_row.append(".")
                    new_row.append(".")
                case "@":
                    new_row.append("@")
                    new_row.append(".")
        new_maze.append(new_row)
    return new_maze


def push_BIG_boxes(
    maze: list[list[str]],
    coord: tuple[int, int],
    direction: tuple[int, int],
    apply_changes: bool,
) -> bool:
    def is_within_bounds(coord: tuple[int, int]) -> bool:
        return (
            coord[0] >= 0
            and coord[0] < len(maze)
            and coord[1] >= 0
            and coord[1] < len(maze[1])
        )

    row, col = coord
    prev_row, prev_col = row - direction[0], col - direction[1]
    next_row, next_col = row + direction[0], col + direction[1]

    if not is_within_bounds(coord) or maze[row][col] == "#":
        return False

    if maze[row][col] == ".":
        if apply_changes:
            maze[prev_row][prev_col], maze[row][col] = (
                maze[row][col],
                maze[prev_row][prev_col],
            )
        return True

    can_move = False
    if (maze[row][col] == "[" or maze[row][col] == "]") and (
        direction == UP or direction == DOWN
    ):
        if maze[row][col] == "[":
            can_move_left = push_BIG_boxes(
                maze, (next_row, next_col), direction, apply_changes
            )
            can_move_right = push_BIG_boxes(
                maze, (next_row, next_col + 1), direction, apply_changes
            )
            if can_move_left and can_move_right:
                can_move = True
        if maze[row][col] == "]":
            can_move_left = push_BIG_boxes(
                maze, (next_row, next_col - 1), direction, apply_changes
            )
            can_move_right = push_BIG_boxes(
                maze, (next_row, next_col), direction, apply_changes
            )
            if can_move_left and can_move_right:
                can_move = True
    else:
        can_move = push_BIG_boxes(maze, (next_row, next_col), direction, apply_changes)

    if can_move and apply_changes:
        maze[prev_row][prev_col], maze[row][col] = (
            maze[row][col],
            maze[prev_row][prev_col],
        )
    return can_move


def part2(maze: list[list[str]], instructions: str) -> int:
    maze = transform_maze(maze)
    r, c = find_robot(maze)

    for i in instructions:
        if i == "\n":
            continue
        # print((r, c), i)
        direction = sym_to_dir[i]
        new_r, new_c = (r + direction[0], c + direction[1])
        push_succeeded = push_BIG_boxes(maze, (new_r, new_c), direction, False)
        if push_succeeded:
            push_BIG_boxes(maze, (new_r, new_c), direction, True)
            r, c = new_r, new_c
        # for row in maze:
        #     print("".join(row))

    ans = 0
    for ridx, row in enumerate(maze):
        for cidx, tile in enumerate(row):
            if tile == "[":
                ans += 100 * ridx + cidx
    return ans


# 1459111 too high
if __name__ == "__main__":
    maze, instructions = get_input()
    print(part1(deepcopy(maze), instructions))
    print(part2(deepcopy(maze), instructions))
