#include "UUID.h"

std::random_device UUID::rd;
std::mt19937 UUID::gen(UUID::rd());
std::uniform_int_distribution<int> UUID::distrib(0, 15);

std::string UUID::GenerateUUID()
{
    std::stringstream ss;

    ss << std::hex;
    for (int i = 0; i < 8; ++i) {
        ss << distrib(gen);
    }

    ss << '-';
    for (int i = 0; i < 4; ++i) {
        ss << distrib(gen);
    }

    ss << '-';
    for (int i = 0; i < 4; ++i) {
        ss << distrib(gen);
    }

    ss << '-';
    for (int i = 0; i < 12; ++i) {
        ss << distrib(gen);
    }

    return ss.str();
}