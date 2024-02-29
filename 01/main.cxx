#include <iostream>
#include <string>
#include <string_view>
#include <array>
#include <vector>
#include <utility>
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

std::pair<int, int> parseStringNum(const std::string_view s, int pos)
{
    pos += 1;
    int i = 0;

    for (std::string n : DIGIT_NAMES)
    {
        int begin = std::max(pos - static_cast<int>(n.length()), 0);
        int len = pos - begin;

        auto sub = s.substr(begin, len);

        if (sub == n)
        {
            return {i, 0};
        }

        i += 1;
    }

    return {0, 1};
}

std::pair<int, int> parseDigit(const char &c)
{
    if (c >= '0' and c <= '9')
    {
        return {c - ASCII_0, 0};
    }

    return {0, 1};
}

int main(int argc, char const *argv[])
{
    std::string l{};
    int total_sum{};

    while (std::getline(std::cin, l))
    {
        auto l_digits = std::vector<int>{};
        int l_sum{};

        for (int i = 0; i < l.length(); i += 1)
        {
            const auto [pd_r, pd_err] = parseDigit(l[i]);
            if (pd_err == 0)
            {
                l_digits.push_back(pd_r);
                continue;
            }

            const auto [psn_r, psn_err] = parseStringNum(l, i);
            if (psn_err == 0)
            {
                l_digits.push_back(psn_r);
                continue;
            }
        }

        l_sum += l_digits[0];
        l_sum *= 10;
        l_sum += l_digits[l_digits.size() - 1];
        total_sum += l_sum;
    }

    std::cout << total_sum << '\n';
    return 0;
}
