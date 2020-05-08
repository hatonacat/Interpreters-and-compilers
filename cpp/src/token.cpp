#include <iostream>

#include "token.h"

Token::Token(Token_type token_type, std::string token_value)
{
    value = token_value; 
    type = token_type;
}

Token_type Token::get_type()
{
    return type;
}

std::string Token::get_value()
{
    return value;
}

void Token::print_content()
{
    std::string type_name = "None";
    switch(type)
    {
        case DIVIDE: type_name = "DIVIDE"; break;
        case MINUS: type_name = "MINUS"; break;
        case MULTIPLY: type_name = "MULTIPLY"; break;
        case NUMBER: type_name = "NUMBER"; break;
        case PLUS: type_name = "PLUS"; break;
    }
    
    std::cout << "Token(" << value << ", " << type_name << ")" << std::endl; 
}