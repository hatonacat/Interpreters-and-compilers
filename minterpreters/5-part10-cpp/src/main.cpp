#include <iostream>
#include <string>

#include "interpreter.h"
#include "lexer.h"
#include "parser.h"

int main() {
    std::string user_code = R"(
        Begin
            int a = 3*6
        End)";
    std::cout << "Input code: \"" << user_code << "\"\n" << std::endl;

    Interpreter interpreter(user_code);
    interpreter.interpret();
}