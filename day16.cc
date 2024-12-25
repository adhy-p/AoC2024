#include <bits/stdc++.h>

const std::pair<int, int> EAST{0, 1};
const std::pair<int, int> SOUTH{1, 0};
const std::pair<int, int> WEST{0, -1};
const std::pair<int, int> NORTH{-1, 0};
const std::array<std::pair<int, int>, 4> DIRECTIONS = {EAST, SOUTH, WEST,
                                                       NORTH};

using PQ_Item = std::tuple<int, std::pair<int, int>,
                           int>; // (distance, position, direction)

std::ostream &operator<<(std::ostream &out, const std::pair<int, int> &p) {
  out << "(" << p.first << "," << p.second << ")";
  return out;
}

std::ostream &operator<<(
    std::ostream &out,
    const std::priority_queue<PQ_Item, std::vector<PQ_Item>, std::greater<>>
        pq) {
  auto tmp = pq;
  out << "===== PQ =====" << std::endl;
  while (!tmp.empty()) {
    auto [dist, pos, dir] = tmp.top();
    out << dist << " (" << pos.first << "," << pos.second << ") " << dir
        << std::endl;
    tmp.pop();
  }
  out << "==============" << std::endl;
  return out;
}

std::ostream &
operator<<(std::ostream &out,
           const std::vector<std::vector<std::pair<int, int>>> parent) {
  std::cout << "===== Parent =====" << std::endl;
  for (const auto &row : parent) {
    for (const auto &item : row) {
      std::cout << item << " ";
    }
    std::cout << std::endl;
  }
  std::cout << "==============" << std::endl;
  return out;
};

auto find_pos(const std::vector<std::string> &maze,
              const char to_find) -> std::pair<int, int> {
  const int nrows = maze.size();
  const int ncols = maze[0].size();
  for (int i = 0; i < nrows; ++i) {
    for (int j = 0; j < ncols; ++j) {
      if (maze[i][j] == to_find)
        return {i, j};
    }
  }
  assert(false);
  return {-1, -1};
};

auto reconstruct_path(
    const std::vector<std::vector<std::pair<int, int>>> &parents,
    const std::pair<int, int> end_pos) -> std::vector<std::pair<int, int>> {
  std::pair<int, int> curr_pos{end_pos};
  std::vector<std::pair<int, int>> points{};
  while (curr_pos != std::pair<int, int>{-1, -1}) {
    // std::cout << curr_pos << std::endl;
    points.push_back(curr_pos);
    curr_pos = parents[curr_pos.first][curr_pos.second];
  }
  return points;
}

/**
 * Returns the distance between start_pos and end_pos
 * and vector of points that is part of the path
 */
auto dijkstra(const std::vector<std::string> &maze,
              const std::pair<int, int> start_pos,
              const std::pair<int, int> end_pos, const int start_dir)
    -> std::pair<int, std::vector<std::pair<int, int>>> {

  const int nrows = maze.size();
  const int ncols = maze[0].size();

  auto is_within_maze = [nrows, ncols](int row, int col) -> bool {
    return row >= 0 && row < nrows && col >= 0 && col < ncols;
  };

  std::vector<std::vector<int>> distance(
      nrows, std::vector<int>(ncols, std::numeric_limits<int>::max()));
  std::vector<std::vector<std::pair<int, int>>> parent(
      nrows, std::vector<std::pair<int, int>>(ncols, {-1, -1}));

  std::priority_queue<PQ_Item, std::vector<PQ_Item>, std::greater<>> pq;

  distance[start_pos.first][start_pos.second] = 0;
  pq.push({0, start_pos, start_dir});
  while (!pq.empty()) {
    auto [curr_dist, pos, curr_dir] = pq.top();
    pq.pop();
    if (pos == end_pos) {
      // std::cout << parent << std::endl;
      return {curr_dist, reconstruct_path(parent, end_pos)};
    }

    for (int d = 0; d < 4; ++d) {
      int next_row = pos.first + DIRECTIONS[d].first;
      int next_col = pos.second + DIRECTIONS[d].second;
      int next_dist = curr_dist + 1;
      switch (abs(curr_dir - d)) {
      case 1:
      case 3:
        next_dist += 1000;
        break;
      case 2:
        next_dist += 2000;
        break;
      };
      if (is_within_maze(next_row, next_col) &&
          maze[next_row][next_col] != '#' &&
          next_dist < distance[next_row][next_col]) {
        distance[next_row][next_col] = next_dist;
        parent[next_row][next_col] = pos;
        pq.push({next_dist, {next_row, next_col}, d});
      }
    }
    // std::cout << pq << std::endl;
  }
  assert(false);
  return {0, {}};
}

/**
 * we consider the shortest distance between two points
 * for each directions
 */
auto four_sides_dijkstra(const std::vector<std::string> &maze,
                         const std::pair<int, int> start_pos,
                         const std::pair<int, int> end_pos, const int start_dir)
    -> std::pair<std::vector<std::vector<std::vector<int>>>,
                 std::vector<std::pair<int, int>>> {

  const int nrows = maze.size();
  const int ncols = maze[0].size();

  auto is_within_maze = [nrows, ncols](int row, int col) -> bool {
    return row >= 0 && row < nrows && col >= 0 && col < ncols;
  };

  // main difference compared to standard dijkstra
  std::vector<std::vector<std::vector<int>>> distance(
      nrows, std::vector<std::vector<int>>(
                 ncols, std::vector<int>(4, std::numeric_limits<int>::max())));
  std::vector<std::vector<std::pair<int, int>>> parent(
      nrows, std::vector<std::pair<int, int>>(ncols, {-1, -1}));

  std::priority_queue<PQ_Item, std::vector<PQ_Item>, std::greater<>> pq;

  for (int d = 0; d < 4; ++d) {
    int dist = 0;
    switch (abs(start_dir - d)) {
    case 1:
    case 3:
      dist += 1000;
      break;
    case 2:
      dist += 2000;
      break;
    };
    distance[start_pos.first][start_pos.second][d] = dist;
    pq.push({dist, start_pos, d});
  }

  while (!pq.empty()) {
    auto [curr_dist, pos, curr_dir] = pq.top();
    pq.pop();
    if (pos == end_pos) {
      return {distance, reconstruct_path(parent, end_pos)};
    }

    for (int d = 0; d < 4; ++d) {
      int next_row = pos.first + DIRECTIONS[d].first;
      int next_col = pos.second + DIRECTIONS[d].second;
      int next_dist = curr_dist + 1;
      switch (abs(curr_dir - d)) {
      case 1:
      case 3:
        next_dist += 1000;
        break;
      case 2:
        next_dist += 2000;
        break;
      };
      if (is_within_maze(next_row, next_col) &&
          maze[next_row][next_col] != '#' &&
          next_dist < distance[next_row][next_col][d]) {
        distance[next_row][next_col][d] = next_dist;
        if (parent[next_row][next_col] == std::pair<int, int>{-1, -1}) {
          parent[next_row][next_col] = pos;
        }
        pq.push({next_dist, {next_row, next_col}, d});
      }
    }
  }
  assert(false);
  return {{}, {}};
}

auto find_tiles_in_all_shortest_paths(
    const std::vector<std::string> &maze, const std::pair<int, int> start_pos,
    const std::pair<int, int> end_pos) -> int {

  const int nrows = maze.size();
  const int ncols = maze[0].size();

  std::vector<std::vector<bool>> is_in_path(nrows,
                                            std::vector<bool>(ncols, false));
  const auto [dist, shortest_path] =
      four_sides_dijkstra(maze, start_pos, end_pos, 0);

  int target = std::numeric_limits<int>::max();
  for (int d = 0; d < 4; ++d) {
    if (target > dist[end_pos.first][end_pos.second][d]) {
      target = dist[end_pos.first][end_pos.second][d];
    }
  }

  auto add_tiles_to_best_paths =
      [&is_in_path](const std::vector<std::pair<int, int>> &shortest_path) {
        for (const auto [r, c] : shortest_path) {
          is_in_path[r][c] = true;
        }
      };

  add_tiles_to_best_paths(shortest_path);

  int best_tiles = 0;
  for (int r = 0; r < nrows; ++r) {
    for (int c = 0; c < ncols; ++c) {
      if (maze[r][c] != '#' && !is_in_path[r][c]) {
        for (int d = 0; d < 4; ++d) {
          auto [tile_to_end, path] = dijkstra(maze, {r, c}, end_pos, d);
          if (dist[r][c][d] + tile_to_end == target) {
            add_tiles_to_best_paths(path);
          }
        }
      }
      if (is_in_path[r][c]) {
        ++best_tiles;
      }
    }
  }
  return best_tiles;
}

int main() {
  std::ifstream input{"day16.txt"};
  std::string line{};
  std::vector<std::string> maze;
  while (std::getline(input, line)) {
    maze.push_back(std::move(line));
  }

  const auto start = find_pos(maze, 'S');
  const auto end = find_pos(maze, 'E');
  std::cout << "start: " << start << std::endl;
  std::cout << "end: " << end << std::endl;

  auto [dist, path] = dijkstra(maze, start, end, 0);
  // part 1
  std::cout << dist << std::endl;
  // part 2
  std::cout << find_tiles_in_all_shortest_paths(maze, start, end) << std::endl;
  return 0;
}