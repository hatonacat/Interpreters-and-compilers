/**
 * Processes an input string and generates 'Token' objects
 * one at a time when requested.
 * Typically used by a separate Parser module
 **/

#ifndef LEXER_H
#define LEXER_H

#include <map>
#include <string>
#include <set>
#include <unordered_map>

#include "token.h"

class Lexer {
    public:
        Lexer() = default;
        Lexer(std::string user_code="");
        ~Lexer() {};

        std::string protected_check(std::string match_result);

        std::string get_code();
        void set_code(std::string init_code) {code = init_code;};

        Token get_current_token() {return current_token;};
        Token get_next_token();

        int get_pos() {return pos;};
        void set_pos(int new_pos) {pos = new_pos;};


    private:
        std::string code;   // The code to tokenise
        int pos;            // Lexer position in code
        std::map<std::string, std::string> regex_expressions;
        Token current_token;
        std::unordered_map<std::string, std::string> protected_terms;

        // Convert from regex match to a token
        Token tokenise();

        void lexer_error(std::string err_message = "");
};

#endif