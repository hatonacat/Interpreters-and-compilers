/*
A token is used in the calc1 interpreter to store
individual tokenised elements.
*/

#pragma once

#include <iostream>
#include <string>

enum Token_type
{
    None,
    DIVIDE,
    END,
    MINUS,
    MULTIPLY,
    NUMBER,
    PLUS,
};

class Token
{
    public:
        Token() = default;
        Token(Token_type token_type, std::string token_value);
        ~Token() = default;

        std::string get_value();
        Token_type get_type();
        void print_content();

    private:
        std::string value;
        Token_type type;
};



