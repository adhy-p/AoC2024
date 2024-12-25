from itertools import product


def get_input() -> tuple[list]:
    with open("day25.txt", "r") as f:
        locks = []
        keys = []
        items = f.read().split("\n\n")
        for i in items:
            lines = i.splitlines()
            if lines[0] == "#" * 5:
                locks.append(lines)
            elif lines[-1] == "#" * 5:
                keys.append(lines)
            else:
                assert False
        return locks, keys


def has_overlap(lock: list[str], key: list[str]) -> bool:
    for lock_row, key_row in zip(lock, key):
        for lock_item, key_item in zip(lock_row, key_row):
            if lock_item == "#" and key_item == "#":
                return True
    return False


def part1(locks: list[list[str]], keys: list[list[str]]) -> int:
    ans = 0
    for l, k in product(locks, keys):
        if not has_overlap(l, k):
            ans += 1
    return ans


if __name__ == "__main__":
    locks, keys = get_input()
    print(locks, keys)
    print(part1(locks, keys))
