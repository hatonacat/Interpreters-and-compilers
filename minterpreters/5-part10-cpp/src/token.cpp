#include "token.h"

Token::Token(std::string init_type, std::string init_value) {
    type = init_type;
    value = init_value;
};

Token::~Token() {};

std::ostream& operator<<(std::ostream& os, const Token t) {
    os << "Token(" << t.type << ", " << t.value << ")";
    return os;
 };