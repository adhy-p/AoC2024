import re


def get_input() -> None:
    with open("day13.txt", "r") as f:
        lines = f.read().splitlines()
        eq = []
        for i in range(0, len(lines), 4):
            a = re.search(r"X\+(\d+), Y\+(\d+)", lines[i])
            b = re.search(r"X\+(\d+), Y\+(\d+)", lines[i + 1])
            prize = re.search(r"X=(\d+), Y=(\d+)", lines[i + 2])
            eq.append(
                (
                    (int(a.group(1)), int(a.group(2))),
                    (int(b.group(1)), int(b.group(2))),
                    (int(prize.group(1)), int(prize.group(2))),
                )
            )
        return eq


def min_token(a, b, prize):
    min_token = float("inf")
    A_PRICE = 3
    B_PRICE = 1

    """
    let na = # of press of A
    let nb = # of press of B

    eq1 = na * a[0] + nb * b[0] = prize[0]
    eq2 = na * a[1] + nb * b[1] = prize[1]

    eliminate nb: multiply eq1 with b[1] and multiply eq2 with b[0], then substract
    na * a[0] * b[1] - na * a[1] * b[0] = prize[0] * b[1] - prize[1] * b[0]
    na = (prize[0] * b[1] - prize[1] * b[0]) / (a[0] * b[1] - a[1] * b[0])
    """
    eq1 = (a[0], b[0], prize[0])
    eq2 = (a[1], b[1], prize[1])
    # eliminate
    eq1 = tuple(n * b[1] for n in eq1)
    eq2 = tuple(n * b[0] for n in eq2)
    eliminated = tuple(n1 - n2 for n1, n2 in zip(eq1, eq2))

    if eliminated[0] == 0:
        # eq1 = k * eq2
        # infinitely many solutions
        # todo: handle this case
        print(a, b, prize)
        assert False

    na = (prize[0] * b[1] - prize[1] * b[0]) / (a[0] * b[1] - a[1] * b[0])
    nb = (prize[0] - na * a[0]) / b[0]
    if na != int(na) or nb != int(nb):
        # not an integer
        return 0
    return int(na) * A_PRICE + int(nb) * B_PRICE


def part1(eq):
    return sum(min_token(a, b, prize) for a, b, prize in eq)


def part2(eq):
    return sum(
        min_token(a, b, (prize0 + 10000000000000, prize1 + 10000000000000))
        for a, b, (prize0, prize1) in eq
    )


if __name__ == "__main__":
    eq = get_input()
    print(part1(eq))
    print(part2(eq))
