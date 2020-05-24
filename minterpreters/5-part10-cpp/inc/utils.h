/*
 * General utility functions used in the project
 */

#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <map>
#include <iostream>

template <typename T, typename U>
void print_map(std::map<T, U> &map) {
    for (const auto it : map) {
        std::cout << it.first << " = " << it.second << std::endl;
    }
};

std::string upper(std::string str);

#endif