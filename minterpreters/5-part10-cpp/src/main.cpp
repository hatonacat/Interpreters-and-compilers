#include <iostream>
#include <string>

#include "interpreter.h"
#include "lexer.h"
#include "parser.h"

int main() {
    std::string user_code = R"(
        Program matts_program;
        Var
            a : int;
        
        Begin
            real a = (2.1*4.2)/2.0;
            int b = --3*-2;
        End.)";
    std::cout << "Input code: \"" << user_code << "\"\n" << std::endl;

    Interpreter interpreter(user_code);
    interpreter.interpret();
}