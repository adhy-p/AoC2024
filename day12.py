from collections import defaultdict

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)
DIRS = [RIGHT, DOWN, LEFT, UP]


def get_input() -> None:
    with open("day12.txt", "r") as f:
        return f.read().splitlines()


def explore(
    garden: list[str],
    is_visited: list[list[bool]],
    coord: tuple[int, int],
) -> tuple[int, int, set, set]:
    def is_within_bounds(coord: tuple[int, int]) -> bool:
        return (
            coord[0] >= 0
            and coord[0] < len(garden)
            and coord[1] >= 0
            and coord[1] < len(garden[1])
        )

    row, col = coord
    is_visited[row][col] = True

    coords = set()  # all coordinates of the shape
    coords.add((row, col))
    borders = defaultdict(list)  # only borders. coordinate -> sides

    area = 1
    perimeter = 4  # part 1

    for direction in DIRS:
        dr, dc = direction
        new_row = row + dr
        new_col = col + dc
        if (
            is_within_bounds((new_row, new_col))
            and garden[new_row][new_col] == garden[row][col]
        ):
            # part 1
            # side touches another grid -> perimeter -= 1
            perimeter -= 1
            if not is_visited[new_row][new_col]:
                a, p, c, b = explore(garden, is_visited, (new_row, new_col))
                area += a
                perimeter += p
                coords.update(c)
                borders.update(b)
        else:
            borders[(row, col)].append((direction))
    return (area, perimeter, coords, borders)


# part 2
def calc_discounted_perimeter(
    coords: set[tuple[int, int]],
    borders: dict[tuple[int, int], list[tuple[int, int]]],
    start: tuple[int, int],
) -> int:
    """
    Walk the perimeter in clockwise direction
    each time we make a turn, we increase the number of perimeter by 1
    return the total perimeter (# of turns + 1)
    """

    # sort the border so we start each visit from top left
    borders = {k: sorted(v) for k, v in sorted(borders.items())}

    # side -> dir and dir -> side logic
    # if current side is a "RIGHT" (meaning the plant/coordinate has a right wall)
    # then currently we are walking down
    # +-----+
    # |XXXXX|<----- since we are walking in clockwise direction,
    # |XXXXX|       if a coord is bounded by this right wall
    # |XXXXX|       then we are curently going down
    # |XXXXX|
    # +-----+
    #
    # this logic is reversed when we visit the inner perimeter
    side_to_dir = {RIGHT: DOWN, DOWN: LEFT, LEFT: UP, UP: RIGHT}
    dir_to_side = {DOWN: RIGHT, LEFT: DOWN, UP: LEFT, RIGHT: UP}

    def visit_border(curr_pos: tuple[int, int], curr_dir: tuple[int, int]) -> bool:
        # 'visit' a border and remove it from the list
        curr_side = dir_to_side[curr_dir]
        if curr_pos not in borders or curr_side not in borders[curr_pos]:
            return False
        borders[curr_pos].remove(curr_side)
        if not borders[curr_pos]:
            borders.pop(curr_pos)
        return True

    # --- visit outside perimeters ---

    # start a new search
    num_sides = 1
    curr_pos = start
    side = next(
        iter(borders[curr_pos])
    )  # start from a random side of the border of starting point
    curr_dir = side_to_dir[side]
    visit_border(curr_pos, curr_dir)

    """
    logic regarding change of direction.
    if we are currently going towards right/left,
    we need to change dir to up/down, and vice versa

    X1
    Y23

    assuming we start at X, our route is
    X(R) -> 1(R) -> 1(D) -> 3(R) -> 3(D) ->
    3(L) -> 2(L) -> Y(L) -> Y(U) -> X(U)

    1(R) -> 1(D)
    There's nothing when we go right from 1, so we change direction in place

    1(D) -> 3(R) 
    From 1, we go to 2 (because we are moving down)
    However, 2 has no right border.
    We jump to 3
    """
    while borders:
        next_pos = (curr_pos[0] + curr_dir[0], curr_pos[1] + curr_dir[1])
        side = dir_to_side[curr_dir]
        if next_pos in borders and side in borders[next_pos]:
            # continue in the same dir
            curr_pos = next_pos
        elif next_pos not in coords:
            # need to change direction (but stay at the same place)
            # follow clockwise R->D->L->U
            next_dir = {
                RIGHT: DOWN,
                DOWN: LEFT,
                LEFT: UP,
                UP: RIGHT,
            }
            num_sides += 1
            curr_dir = next_dir[curr_dir]
        elif next_pos in coords and (
            next_pos not in borders
            or (next_pos in borders and side not in borders[next_pos])
        ):
            # need to change direction and 'jump' to the next tile
            # change direction to the side we were suppored to visit
            num_sides += 1
            curr_dir = side
            # from next_pos, move one more time to 'jump'
            curr_pos = (next_pos[0] + curr_dir[0], next_pos[1] + curr_dir[1])

        visited = visit_border(curr_pos, curr_dir)
        if not visited and borders:
            # we changed direction at the starting pos and failed to visit
            num_sides -= 1
            break

    if not borders:
        return num_sides

    # --- visit inside perimeters, if any ---

    # need to reverse the logic to counter-clockwise ish
    side_to_dir = {RIGHT: UP, DOWN: RIGHT, LEFT: DOWN, UP: LEFT}
    dir_to_side = {DOWN: LEFT, LEFT: UP, UP: RIGHT, RIGHT: DOWN}

    # starting a new search
    num_sides += 1
    curr_pos = next(iter(borders))
    side = next(iter(borders[curr_pos]))
    curr_dir = side_to_dir[side]
    visit_border(curr_pos, curr_dir)
    while borders:
        next_pos = (curr_pos[0] + curr_dir[0], curr_pos[1] + curr_dir[1])
        side = dir_to_side[curr_dir]
        if next_pos in borders and side in borders[next_pos]:
            # continue in the same dir
            curr_pos = next_pos
        elif next_pos not in coords and (curr_pos in borders):
            next_dir = {
                RIGHT: UP,
                DOWN: RIGHT,
                LEFT: DOWN,
                UP: LEFT,
            }
            num_sides += 1
            curr_dir = next_dir[curr_dir]
        elif next_pos not in coords or (
            next_pos in coords
            and (
                next_pos not in borders
                or (next_pos in borders and side not in borders[next_pos])
            )
        ):
            # need to change direction and 'jump' to the next tile
            # change direction to the side we were suppored to visit
            num_sides += 1
            curr_dir = side
            # from next_pos, move one more time to 'jump'
            curr_pos = (next_pos[0] + curr_dir[0], next_pos[1] + curr_dir[1])

        visited = visit_border(curr_pos, curr_dir)
        if not visited and borders:
            # we changed direction at the starting pos and failed to visit
            # however, we are also starting a new search
            # so num_sides -= 1 and num_sides += 1

            # start a new search
            curr_pos = next(iter(borders))
            side = next(iter(borders[curr_pos]))
            curr_dir = side_to_dir[side]
            visit_border(curr_pos, curr_dir)
    return num_sides


def part1(garden: list[str]) -> int:
    nrows = len(garden)
    ncols = len(garden[0])
    is_visited = [[False for _ in range(ncols)] for _ in range(nrows)]
    ans = 0
    for ridx, row in enumerate(garden):
        for cidx, plant in enumerate(row):
            if not is_visited[ridx][cidx]:
                area, perimeter, _, _ = explore(garden, is_visited, (ridx, cidx))
                ans += area * perimeter
    return ans


def count_corner(coords: set[tuple[int, int]]) -> int:
    """
    a better way for part 2
    number of sides == number of corners
    simply count the number of corners
    .....
    ..0..
    .000.
    ..0..

    outside corners (topright) -> (r-1,c) and (r,c+1) is a different block (or empty space)
    repeat for topleft, bottomleft, bottomright

    inside corners (topright)  -> (r-1,c) and (r,c+1) is the SAME block and (r-1,c+1) is a different one
    """
    perimeter = 0
    for r, c in coords:
        # outside corner
        perimeter += (r - 1, c) not in coords and (r, c - 1) not in coords
        perimeter += (r + 1, c) not in coords and (r, c - 1) not in coords
        perimeter += (r - 1, c) not in coords and (r, c + 1) not in coords
        perimeter += (r + 1, c) not in coords and (r, c + 1) not in coords
        # Inner corners
        perimeter += (
            (r - 1, c) in coords
            and (r, c - 1) in coords
            and (r - 1, c - 1) not in coords
        )
        perimeter += (
            (r + 1, c) in coords
            and (r, c - 1) in coords
            and (r + 1, c - 1) not in coords
        )
        perimeter += (
            (r - 1, c) in coords
            and (r, c + 1) in coords
            and (r - 1, c + 1) not in coords
        )
        perimeter += (
            (r + 1, c) in coords
            and (r, c + 1) in coords
            and (r + 1, c + 1) not in coords
        )
    return perimeter


def part2(garden: list[str]) -> int:
    nrows = len(garden)
    ncols = len(garden[0])
    is_visited = [[False for _ in range(ncols)] for _ in range(nrows)]
    ans = 0
    for ridx, row in enumerate(garden):
        for cidx, plant in enumerate(row):
            if not is_visited[ridx][cidx]:
                area, _, coords, borders = explore(garden, is_visited, (ridx, cidx))
                # discounted_perimeter = calc_discounted_perimeter(
                #     coords, borders, (ridx, cidx)
                # )
                discounted_perimeter = count_corner(coords)
                ans += area * discounted_perimeter
    return ans


if __name__ == "__main__":
    garden = get_input()
    print(part1(garden))
    print(part2(garden))
