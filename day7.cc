#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using equation = std::pair<long, std::vector<long>>;

bool is_possible(const long lhs, const std::vector<long> &rhs, long current_sum,
                 long index) {
  if (current_sum > lhs || index == rhs.size()) {
    return current_sum == lhs;
  }
  // add & multiply + concatenate
  bool ok = is_possible(lhs, rhs, current_sum + rhs[index], index + 1) ||
            is_possible(lhs, rhs, current_sum * rhs[index], index + 1);

  if (ok)
    return true;

  auto get_digits = [](int x) {
    int num_digits = 0;
    while (x) {
      x /= 10;
      num_digits += 1;
    }
    return num_digits;
  };

  int num_digits = get_digits(rhs[index]);
  return is_possible(
      lhs, rhs, current_sum * std::pow(10, num_digits) + rhs[index], index + 1);
}

long part1(const std::vector<equation> &equations) {
  long ans = 0;
  for (const auto &[lhs, rhs] : equations) {
    if (is_possible(lhs, rhs, 0, 0)) {
      ans += lhs;
    }
  }
  return ans;
}

int main() {
  std::ifstream input{"day7.txt"};
  std::string line{};
  std::vector<equation> equations;
  while (std::getline(input, line)) {
    long colon = line.find(':');
    std::string result(line.begin(), line.begin() + colon);
    std::string operands_str(line.begin() + colon + 1, line.end());

    std::string number{};
    std::stringstream ss{operands_str};
    std::vector<long> operands_long;
    while (ss >> number) {
      operands_long.push_back(std::stoi(number));
    }
    equations.push_back({std::stol(result), operands_long});
  }
  std::cout << part1(equations) << std::endl;
  return 0;
}