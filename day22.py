from collections import deque, defaultdict


def get_input() -> tuple[list[list[str]], list[str]]:
    with open("day22.txt", "r") as f:
        return [int(n) for n in f.read().splitlines()]


MOD = 16777216


def gen_next_secret(secret: int):
    result = secret * 64
    secret ^= result
    secret %= MOD

    result = secret // 32
    secret ^= result
    secret %= MOD

    result = secret * 2048
    secret ^= result
    secret %= MOD

    return secret


def part1(secrets: list[str]) -> int:
    for _ in range(2000):
        for i in range(len(secrets)):
            secrets[i] = gen_next_secret(secrets[i])
    return sum(secrets)


seq_dict = defaultdict(dict)


def part2(secrets: list[str]) -> int:
    sequences = [deque() for _ in range(len(secrets))]
    for _ in range(2000):
        for i in range(len(secrets)):
            next_secret = gen_next_secret(secrets[i])
            diff = (next_secret % 10) - (secrets[i] % 10)
            price = next_secret % 10

            sequences[i].append(diff)
            if len(sequences[i]) > 4:
                sequences[i].popleft()
            if len(sequences[i]) == 4:
                seq = tuple(sequences[i])
                if seq not in seq_dict or i not in seq_dict[seq]:
                    seq_dict[seq][i] = price

            # print(
            #     f"{i}: {secrets[i]} -> {next_secret}. diff: {diff}, price: {price}"
            # )
            # print(sequences[i])

            secrets[i] = next_secret
    return max(sum(i for i in v.values()) for v in seq_dict.values())


if __name__ == "__main__":
    secrets = get_input()
    print(part1(secrets.copy()))
    print(part2(secrets))
