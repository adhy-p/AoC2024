from typing import List
from collections import Counter

f = open("day11.txt", "r")
input = f.read().split(" ")
f.close()

input = Counter(int(i) for i in input)


def get_ndigits(n):
    digits = 0
    while n > 0:
        n //= 10
        digits += 1
    return digits


def process(num: int) -> List[int]:
    if num == 0:
        return [1]
    ndigits = get_ndigits(num)
    if ndigits % 2 == 0:
        half_digits = 10 ** (ndigits // 2)
        return [num // half_digits, num % half_digits]
    return [num * 2024]


print(input)

tmp = Counter()
for i in range(75):
    for num, count in input.items():
        out = process(num)
        for item in out:
            tmp[item] += count
    input = tmp
    tmp = Counter()

print(sum(input.values()))
