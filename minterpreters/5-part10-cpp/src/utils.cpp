#include "utils.h"

std::string upper(std::string str) {
    for (int i = 0; i < str.length(); ++i) {
        str[i] = std::toupper(str[i]);
    };
    return str;
}