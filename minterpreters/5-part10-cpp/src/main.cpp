#include <iostream>
#include <string>

#include "interpreter.h"
#include "lexer.h"
#include "parser.h"

int main() {
    std::string my_code = "1*2";
    std::cout << "Input code: \"" << my_code << "\"" << std::endl;

    Lexer lexer(my_code);
    Parser parser(&lexer);
    Interpreter interpreter(&parser);

    interpreter.interpret();
}