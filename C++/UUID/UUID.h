#pragma once

#include <random>
#include <sstream>
#include <string>

class UUID
{
    static std::random_device rd;
    static std::mt19937 gen;
    static std::uniform_int_distribution<int> distrib;

public:
    static std::string GenerateUUID();
};
