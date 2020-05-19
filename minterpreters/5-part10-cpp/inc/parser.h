/**
 * Converts a token stream into an intermediate AST representation 
**/

#ifndef PARSER_H
#define PARSER_H

#include <string>
#include <memory>

#include "ast_visitor.h"
#include "lexer.h"
#include "token.h"

class Parser {
    public:
        Parser(std::string user_code);
        ~Parser();

        // Convert Token stream into AST and return pointer to head
        AST* parse();
        void parsing_error(std::string err_message);

    private:
        Lexer *lexer;

        /*
        * GRAMMARS
        */
        void eat(std::string);
        AST* assign_op();
        AST* term();
        AST* factor();
};

#endif