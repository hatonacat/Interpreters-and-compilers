#include <iostream>
#include <string>

#include "interpreter.h"
#include "lexer.h"
#include "parser.h"

int main() {
    std::string user_code = "int a =1*2";
    std::cout << "Input code: \"" << user_code << "\"" << std::endl;

    Interpreter interpreter(user_code);
    interpreter.interpret();
}