#include <algorithm>
#include <cmath>
#include <deque>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

using tii = std::tuple<int, int, int>;

long part1(std::deque<tii> empty_blocks, std::deque<tii> files) {
  long ans{0};
  int processsed_block{0};

  while (!files.empty()) {
    // file
    auto [file_id, file_start_idx, file_len] = files[0];
    files.pop_front();
    for (int i = 0; i < file_len; ++i) {
      ans += file_id * processsed_block;
      ++processsed_block;
    }
    // empty
    auto [_empty, empty_start_idx, empty_len] = empty_blocks[0];
    empty_blocks.pop_front();
    while (!files.empty() && empty_len > 0) {
      auto [file_id, file_start_idx, file_len] = files[files.size() - 1];
      if (file_len > empty_len) {
        // modify file arr in-place
        for (int i = 0; i < empty_len; ++i) {
          ans += file_id * processsed_block;
          ++processsed_block;
        }
        files[files.size() - 1] = {file_id, file_start_idx,
                                   file_len - empty_len};
        empty_len = 0;
      } else {
        // pop and get next file from the back
        for (int i = 0; i < file_len; ++i) {
          ans += file_id * processsed_block;
          ++processsed_block;
        }
        empty_len -= file_len;
        files.pop_back();
      }
    }
  }
  return ans;
}

long part2(std::deque<tii> empty_blocks, std::deque<tii> files) {
  long ans{};
  for (int i = files.size() - 1; i >= 0; --i) {
    // find and move to empty space
    auto &[file_id, file_start_idx, file_len] = files[i];
    for (auto &[_, empty_start_idx, empty_len] : empty_blocks) {
      if (empty_start_idx >= file_start_idx)
        break;
      if (empty_len >= file_len) {
        file_start_idx = empty_start_idx;
        empty_start_idx += file_len;
        empty_len -= file_len;
        break;
      }
    }
  }
  std::sort(files.begin(), files.end(), [](tii &lhs, tii &rhs) {
    auto [_, i, _] = lhs;
    auto [_, j, _] = rhs;
    return i < j;
  });

  for (const auto [file_id, idx, file_len] : files) {
    for (int i = 0; i < file_len; ++i) {
      ans += file_id * (idx + i);
    }
  }
  return ans;
}

int main() {
  std::ifstream input{"day9.txt"};
  std::string line{};
  std::getline(input, line);
  std::deque<tii> empty_blocks; // (start_idx, len)
  std::deque<tii> files;        // (file_id, start_idx, len)

  int file_id{0};
  long read_disk{0};

  for (int i = 0; i < line.size(); i++) {
    int block_sz = line[i] - '0';
    if (i % 2 == 0) {
      files.push_back({file_id, read_disk, block_sz});
      ++file_id;
    } else {
      empty_blocks.push_back({-1, read_disk, block_sz});
    }
    read_disk += block_sz;
  }

  std::cout << part1(empty_blocks, files) << std::endl;
  std::cout << part2(empty_blocks, files) << std::endl;
  return 0;
}