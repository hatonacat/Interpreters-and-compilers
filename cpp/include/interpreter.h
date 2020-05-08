/*
Interprets a pascal arithmetic equation
into a cpp output.
*/

#pragma once

#include <string>
#include <vector>

#include "token.h"

class Interpreter
{
    public:
        // CONSTRUCTORS AND DESTRUCTORS
        Interpreter() = default;
        Interpreter(std::string user_code_input);
        ~Interpreter() = default;
    
        // STANDARD PUBLIC METHODS
        void add_user_input(std::string user_code_input);   // Only required if not initialised with a value
        Token get_next_token();                             // Retrieves the next token
        void expr();                                        // Parse and execute user code
        void print_tokens();                                // Print current contents of token vector
        void tokenise();                                    // Turn user input into vector of tokens

    private:
        // PRIVATE PARAMETERS
        int pc = 0;                 // program counter
        int token_count = 0;        // tracks tokens issued
        char current_char;          // character at pc position
        Token current_token;
        std::string code_input;     // user input
        std::vector<Token> tokens;

        // STANDARD PRIVATE METHODS
        void advance(int num=1);    // Advances the program counter on request
        void eat(Token_type type, Token token);             // Checks if token matches the expected type and eats it if true
        void parse_error();
        std::string get_number();   // If a numerical char is found, search until the end of the number
        void whitespace();          // If whitespace is found, skip to next valid character
};