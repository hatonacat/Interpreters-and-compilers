/**
 * Converts a token stream into an intermediate AST representation 
**/

#ifndef PARSER_H
#define PARSER_H

#include <string>

#include "ast_visitor.h"
#include "token.h"

class Lexer;

class Parser {
    public:
        Parser(Lexer *init_lexer);
        ~Parser() {};

        // Convert Token stream into AST and return pointer to head
        AST* parse();
        void parsing_error(std::string err_message);

    private:
        Lexer *lexer = nullptr;

        /*
        * GRAMMARS
        */
        void eat(std::string);
        AST* term();
        AST* factor();
};

#endif