/*
Interprets a pascal arithmetic equation
into a cpp output.
*/

#include <ctype.h>
#include <iostream>

#include "interpreter.h"

// CONSTRUCTOR AND DESTRUCTORS =================================

Interpreter::Interpreter(std::string user_code_input)
{
    code_input = user_code_input;
    current_char = code_input[pc];
}

// STANDARD PUBLIC METHODS ======================================

// Take user code and store in internal variable
void Interpreter::add_user_input(std::string user_code_input)
{
    code_input = user_code_input;
    current_char = code_input[pc];
}

Token Interpreter::get_next_token()
{
    current_token = tokens[token_count];
    token_count++;
    return current_token;
}

// Parse and execute user code
void Interpreter::expr()
{
    Token left = get_next_token();
    eat(NUMBER, left);

    float result = stoi(left.get_value());
    while(current_token.get_type() != END)
    {
        Token op = current_token;
        if (op.get_type() == MINUS) {
            eat(MINUS, current_token);
        }
        else if (op.get_type() == PLUS) {
            eat(PLUS, current_token);
        } 
        else if (op.get_type() == MULTIPLY) {
            eat(MULTIPLY, current_token);
        } 
        else if (op.get_type() == DIVIDE) {
            eat(DIVIDE, current_token);
        } 
        else {
            parse_error();
        }

        Token right = current_token;
        eat(NUMBER, right);

        if (op.get_type() == PLUS)
        {
            result += stoi(right.get_value());
        } 
        else if (op.get_type() == MINUS)
        {
            result -= stoi(right.get_value());
        } 
        else if (op.get_type() == MULTIPLY)
        {
            result = result * stoi(right.get_value());
        } 
        else if (op.get_type() == DIVIDE)
        {
            result = result / stoi(right.get_value());
        } 
    }

    std::cout << result << std::endl;
}

// Prints the contents of the tokens vector in a readable format
void Interpreter::print_tokens()
{
    for (auto &token: tokens)
    {
        token.print_content();
    }
    std::cout << std::endl;
}

// Transform the user input into a series of tokens
void Interpreter::tokenise()
{
    while (pc < code_input.size())
    {
        current_char = code_input[pc];  

        if (current_char==' ')
        {
            whitespace();
        }
        else if (isdigit(current_char))
        {
            std::string number = get_number();
            tokens.push_back(Token(NUMBER, number));     
        }
        else if (current_char=='+')
        {
            tokens.push_back(Token(PLUS, "+"));                 
            advance();            
        }
        else if (current_char=='-')
        {
            tokens.push_back(Token(MINUS, "-"));     
            advance();            
        }
        else if (current_char=='*')
        {
            tokens.push_back(Token(MULTIPLY, "*"));     
            advance();            
        }
        else if (current_char=='/')
        {
            tokens.push_back(Token(DIVIDE, "/"));     
            advance();            
        }
        else
        {
            std::cout << "Not implemented: " << current_char << std::endl;
            advance();
        }
    }
    tokens.push_back(Token(END, "END"));
}

// STANDARD PRIVATE METHODS ====================================

// Advance the program counter and current_char by either 1 (default) or a request amount
void Interpreter::advance(int num /*=1*/)
{
    pc += num;
    current_char = code_input[pc];
}

// Checks if token matches the expected type and eats it if true
void Interpreter::eat(Token_type type, Token token)
{
    if (type == token.get_type())
    {
        current_token = get_next_token();
    }
    else
    {
        parse_error();
    }
}

void Interpreter::parse_error()
{
    std::cout << "Error parsing input\n";
    exit(EXIT_FAILURE);
}

// If a numerical char is found, search until the end of the number
std::string Interpreter::get_number()
{
    std::string number = "";
    while (pc < code_input.size() && isdigit(current_char))
    {
        number += current_char;
        advance();
    }

    return number;
}       

// If whitespace is found, skip to next valid character
void Interpreter::whitespace()
{
    while (pc < code_input.size() && current_char == ' ')
    {
        advance();
    }
}