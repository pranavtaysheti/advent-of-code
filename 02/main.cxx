#include <iostream>
#include <vector>
#include <string>
#include <string_view>
#include <algorithm>

constexpr int MAX_RED = 12;
constexpr int MAX_GREEN = 13;
constexpr int MAX_BLUE = 14;

enum Color
{
    cNONE,
    cRED,
    cGREEN,
    cBLUE,
};

struct Balls
{
    Color color{};
    int quantity{};
};

struct GameRecordSubset
{
    int Red{};
    int Green{};
    int Blue{};
};

typedef std::vector<GameRecordSubset> GameRecord;

std::vector<std::string_view> splitString(const std::string_view s, const char d)
// Splits string at delimiter.
{
    auto result = std::vector<std::string_view>{};
    size_t start_pos = 0;
    size_t end_pos = start_pos;

    while (start_pos < s.length())
    {
        const size_t end_pos = std::min(s.find_first_of(d, start_pos), s.length());
        const size_t sub_str_len = end_pos - start_pos;

        const auto sub_str = s.substr(start_pos, sub_str_len);
        result.push_back(sub_str);

        start_pos = end_pos + 2;
    }

    return result;
}

int getGameID(const std::string_view s)
// Parses gameID from the string.
{
    const size_t colon_pos = s.find_first_of(':');
    const size_t id_len = colon_pos - 5;
    const auto id_str = std::string(s.substr(5, id_len));
    return std::stoi(id_str);
}

int getBallsQty(std::string_view s)
{
    const size_t space_pos = s.find_first_of(' ');
    const auto qty_str = std::string(s.substr(0, space_pos));

    return std::stoi(qty_str);
}

Color getBallsColor(std::string_view s)
{
    const size_t space_pos = s.find_first_of(' ');
    const auto color_str = s.substr(space_pos + 1);

    if (color_str == "red")
    {
        return cRED;
    }
    if (color_str == "green")
    {
        return cGREEN;
    }
    if (color_str == "blue")
    {
        return cBLUE;
    }

    return cNONE;
}

Balls getBallsInfo(std::string_view s)
{
    auto result = Balls{};
    result.quantity = getBallsQty(s);
    result.color = getBallsColor(s);

    return result;
}

GameRecordSubset getGameRecordSubset(const std::string_view s)
{
    auto result = GameRecordSubset{};
    const auto vec_colors_str = splitString(s, ',');
    for (const auto color_str : vec_colors_str)
    {
        const auto ballsInfo = getBallsInfo(color_str);

        switch (ballsInfo.color)
        {
        case cRED:
            result.Red = ballsInfo.quantity;
            break;
        case cGREEN:
            result.Green = ballsInfo.quantity;
            break;
        case cBLUE:
            result.Blue = ballsInfo.quantity;
        case cNONE:
        default:
            break;
        }
    }

    return result;
}

GameRecord getGameRecord(const std::string_view s)
// Parses records from the string and returns.
{
    auto result = GameRecord{};
    const size_t start_pos = s.find_first_of(':') + 2;
    const auto gr_str = s.substr(start_pos);
    const auto vec_gsr_str = splitString(gr_str, ';');

    for (const auto gsr_str : vec_gsr_str)
    {
        result.push_back(getGameRecordSubset(gsr_str));
    }

    return result;
}

bool checkGame(const GameRecord &gr)
{
    for (const auto &r : gr)
    {
        if (r.Red > MAX_RED or r.Green > MAX_GREEN or r.Blue > MAX_BLUE)
        {
            return false;
        }
    }

    return true;
}

int main(int argc, char const *argv[])
{
    int sum = 0;
    std::string l{};

    while (std::getline(std::cin, l))
    {
        const auto id = getGameID(l);
        const auto grs = getGameRecord(l);
        if (checkGame(grs))
        {
            sum += id;
        }
    }

    std::cout << sum << '\n';
    return 0;
}
