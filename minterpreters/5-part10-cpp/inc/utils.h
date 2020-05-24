/*
 * General utility functions used in the project
 */

#include <string>

template <typename T, typename U>
void print_map(std::map<T, U> &map) {
    for (const auto it : map) {
        std::cout << it.first << " = " << it.second << std::endl;
    }
};

std::string upper(std::string str) {
    for (int i = 0; i < str.length(); ++i) {
        str[i] = std::toupper(str[i]);
    };
    return str;
}