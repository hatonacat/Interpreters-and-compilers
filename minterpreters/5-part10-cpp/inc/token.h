/**
 * A simple container for Token objects used in Lexers
**/

#ifndef TOKEN_H
#define TOKEN_H

#include <string>
#include <iostream>
#include "token.h"

class Token {
    public:
        Token(std::string type = "NONE", std::string value = "NONE");
        ~Token();

        friend std::ostream& operator<<(std::ostream& os, const Token t);

        std::string get_value() {return value;};
        std::string get_type() {return type;};

    private:
        std::string type;
        std::string value;
};
#endif