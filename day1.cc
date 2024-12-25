#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>

int main() {
  std::vector<int> list1{};
  std::vector<int> list2{};
  std::unordered_map<int, int> counts;

  std::ifstream input{"input"};

  int n1, n2;
  while (input >> n1 >> n2) {
    list1.push_back(n1);
    list2.push_back(n2);
    counts[n2]++;
  }

  std::sort(list1.begin(), list1.end());
  std::sort(list2.begin(), list2.end());

  int diff{};
  int similarity{};
  for (int i = 0; i < list1.size(); ++i) {
    diff += std::abs(list1[i] - list2[i]);
    similarity += list1[i] * counts[list1[i]];
  }
  std::cout << diff << std::endl;
  std::cout << similarity << std::endl;
  return 0;
}
