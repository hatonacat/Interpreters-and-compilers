#include <iostream>
#include <string>

#include "interpreter.h"
#include "lexer.h"
#include "parser.h"

int main() {
    std::string user_code = R"(
        Begin
            Begin
                int a = (2+3)*4;
                int b = 17*23+2;
            End;
        End)";
    std::cout << "Input code: \"" << user_code << "\"\n" << std::endl;

    Interpreter interpreter(user_code);
    interpreter.interpret();
}