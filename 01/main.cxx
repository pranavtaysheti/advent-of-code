#include <iostream>
#include <string>
#include <string_view>
#include <array>
#include <vector>
#include <algorithm>

constexpr int ASCII_0 = 48;
const auto DIGIT_NAMES = std::array<std::string, 10>{
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
};

int parseStringNum(const std::string_view s, int pos)
{
    pos += 1;

    int i = 0;
    for (std::string n : DIGIT_NAMES)
    {
        int begin = std::max(pos - static_cast<int>(n.length()), 0);
        int len = pos - begin;

        auto sub = s.substr(begin, len);

        if (sub == n)
            return i;

        i += 1;
    }

    return -1;
}

int parseDigit(const char c)
{
    if (c >= '0' and c <= '9')
        return c - ASCII_0;

    return -1;
}

std::vector<int> calculateP1(std::string_view s)
{
    std::vector<int> result = {};

    for (const auto c : s)
    {
        auto n = parseDigit(c);
        if (n >= 0)
            result.push_back(n);
    }

    return result;
}

std::vector<int> calculateP2(std::string_view s)
{
    std::vector<int> result = {};

    for (int i = 0; i < s.length(); i += 1)
    {
        auto n = parseDigit(s[i]);
        if (n >= 0)
        {
            result.push_back(n);
            continue;
        }

        n = parseStringNum(s, i);
        if (n >= 0)
            result.push_back(n);
    }

    return result;
}

int solveNumVector(const std::vector<int> &vn)
{
    return 10 * vn.at(0) + vn.back();
}

int main(int argc, char const *argv[])
{
    std::string l{};
    int total_p1_sum = 0;
    int total_p2_sum = 0;

    while (std::getline(std::cin, l))
    {
        total_p1_sum += solveNumVector(calculateP1(l));
        total_p2_sum += solveNumVector(calculateP2(l));
    }

    std::cout << "P1: " << total_p1_sum << '\n';
    std::cout << "P2: " << total_p2_sum << '\n';
    return 0;
}
