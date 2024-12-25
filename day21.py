from collections import deque

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)
DIRS = [RIGHT, DOWN, LEFT, UP]


DIR_TO_SYM = {UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">"}

NUMERIC_KEYPAD = [list("789"), list("456"), list("123"), list("X0A")]
DIRECTIONAL_KEYPAD = [list("X^A"), list("<v>")]


def get_input() -> tuple[list[list[str]], list[str]]:
    with open("day21.txt", "r") as f:
        return f.read().splitlines()


def is_within_bounds(maze: list[list[str]], coord: tuple[int, int]) -> bool:
    return (
        coord[0] >= 0
        and coord[0] < len(maze)
        and coord[1] >= 0
        and coord[1] < len(maze[1])
    )


def find_input_sequence(target_sequence, keypad, start):
    if len(target_sequence) == 1 and keypad[start[0]][start[1]] == target_sequence:
        return ["A"]
    visited = set()
    to_process = deque()

    to_process.append((start, "", 0))  # pos, instructions so far, covered numbers
    visited.add((start, 0))

    out = []

    while to_process:
        (row, col), instr, n_covered = to_process.popleft()
        visited.add(((row, col), n_covered))
        # print((row, col), instr, n_covered)
        if n_covered == len(target_sequence):
            if not out or len(out[-1]) == len(instr):
                out.append(instr)
        for d in DIRS:
            next_row, next_col = row + d[0], col + d[1]
            if is_within_bounds(keypad, (next_row, next_col)):
                if keypad[next_row][next_col] == "X":
                    continue
                next_instr = instr + DIR_TO_SYM[d]
                next_ncovered = n_covered
                while (
                    next_ncovered < len(target_sequence)
                    and keypad[next_row][next_col] == target_sequence[next_ncovered]
                ):  # append A
                    next_instr = next_instr + "A"
                    next_ncovered += 1
                if ((next_row, next_col), next_ncovered) not in visited:
                    to_process.append(((next_row, next_col), next_instr, next_ncovered))
                    # visited.add(((next_row, next_col), next_ncovered))
    # return set(out)
    return out


def part1(instructions: list[str]) -> int:
    ans = 0
    # find the shortest path from one key to the other
    # in the numeric keypad
    path = {}
    for r1, src_row in enumerate(DIRECTIONAL_KEYPAD):
        for c1, src in enumerate(src_row):
            for _r2, target_row in enumerate(DIRECTIONAL_KEYPAD):
                for _c2, target in enumerate(target_row):
                    if src == "X" or target == "X":
                        continue
                    seq = find_input_sequence(target, DIRECTIONAL_KEYPAD, (r1, c1))
                    if len(seq) == 1:
                        path[(src, target)] = seq[0]
                    else:
                        # if there are more than one possibilities to construct target
                        # we try to construct again and find which one is the best
                        best_sequence = None
                        best_sequence_len = float("inf")
                        for s in seq:
                            one_lv_below = find_input_sequence(
                                s, DIRECTIONAL_KEYPAD, (0, 2)
                            )
                            if (
                                not best_sequence
                                or best_sequence
                                and len(one_lv_below[0]) < best_sequence_len
                            ):
                                best_sequence = s
                                best_sequence_len = len(one_lv_below[0])
                        path[(src, target)] = best_sequence
    # print(path)
    for i in instructions:
        seq = find_input_sequence(i, NUMERIC_KEYPAD, (3, 2))
        print(seq)

        for j in range(25):
            print(f"iter {j}")
            out = []
            for s in seq:
                tmp = []
                prev = "A"
                for chr in s:
                    tmp += path[(prev, chr)]
                    prev = chr
                out.append(tmp)
            min_len = min(len(s) for s in out)
            seq = [s for s in out if len(s) == min_len]
            print("seq len: ", len(seq), len(seq[0]))
        min_len = min(len(s) for s in seq)
        print(min_len, int(i[:-1]))
        ans += int(i[:-1]) * min_len
    return ans


def part2(instructions: list[str]) -> int:
    ans = 0
    return ans


if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))
