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

template <typename T>
T BinOpCalc(T left, std::string op_type, T right) {
    T total;
    if (op_type == "MUL") {
        total = left * right;
    }
    else if (op_type == "DIV") {
        total = left / right;
    }
    else if (op_type == "PLUS") {
        total = left + right;
    }
    else if (op_type == "MINUS") {
        total = left - right;
    }
    else {
        std::cout << "No valid binary operation found" << std::endl;
    }

    return total;
};

#endif