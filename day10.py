from collections import deque, defaultdict

f = open("day10.txt", "r")
in_map = f.read().splitlines()
f.close()

to_process = deque()

for ridx, row in enumerate(in_map):
    for cidx, height in enumerate(row):
        if height == "0":
            to_process.append((ridx, cidx, 0, (ridx, cidx)))

ans_map = defaultdict(set)
ans = 0
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
while to_process:
    r, c, height, orig = to_process.popleft()
    if height == 9:
        ans += 1
        ans_map[orig].add((r, c))
        continue
    for dr, dc in directions:
        new_row = r + dr
        new_col = c + dc
        if (
            new_row >= 0
            and new_row < len(in_map)
            and new_col >= 0
            and new_col < len(in_map[0])
        ) and int(in_map[new_row][new_col]) == height + 1:
            to_process.append((new_row, new_col, height + 1, orig))
print(sum(len(m) for m in ans_map.values()))
print(ans)
