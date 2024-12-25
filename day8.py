from collections import defaultdict
from itertools import product
import numpy as np

f = open("day8.txt", "r")
in_map = f.read().splitlines()
f.close()

antennas = defaultdict(list)

for ridx, row in enumerate(in_map):
    for cidx, char in enumerate(row):
        if char.isalnum():
            antennas[char].append((ridx, cidx))

antinodes = set()
for freq, points in antennas.items():
    for p1, p2 in product(points, points):
        if p1 != p2:
            antinodes.add(p1)
            antinodes.add(p1)

            delta = np.subtract(p1, p2)
            antinode1 = np.add(p1, delta)
            antinode2 = np.subtract(p2, delta)

            def inside(pos):
                return (
                    pos[0] >= 0
                    and pos[0] < len(in_map)
                    and pos[1] >= 0
                    and pos[1] < len(in_map[0])
                )

            while inside(antinode1):
                antinodes.add(tuple(antinode1))
                antinode1 = np.add(antinode1, delta)
            while inside(antinode2):
                antinodes.add(tuple(antinode2))
                antinode2 = np.subtract(antinode2, delta)

print(len(antinodes))
