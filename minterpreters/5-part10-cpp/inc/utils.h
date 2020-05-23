/*
 * General utility functions used in the project
 */

template <typename T, typename U>
void print_map(std::map<T, U> &map) {
    for (const auto it : map) {
        std::cout << it.first << " = " << it.second << std::endl;
    }
};