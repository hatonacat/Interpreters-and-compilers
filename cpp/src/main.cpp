#include <iostream>
#include <string>

#include "interpreter.h"

int main()
{
    // Take user input
    std::string user_input;
    while(1)
    {        
        std::cout << "Enter equation > ";
        getline(std::cin, user_input);

        if(user_input == "quit")
        {
            exit(EXIT_SUCCESS);
        }

        // Initialise interpreter object
        Interpreter interpreter;

        // Pass input interpreter and tokenise the input
        interpreter.add_user_input(user_input);
        interpreter.tokenise();

        //interpreter.print_tokens();

        // Pass to expr to parse and interpret result
        interpreter.expr();
    }
};