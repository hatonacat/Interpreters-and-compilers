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
        std::shared_ptr<AST> parse();
        void parsing_error(std::string err_message);

    private:
        std::unique_ptr<Lexer> lexer;

        /*
        * GRAMMARS
        */
        void eat(std::string);
        std::shared_ptr<AST> compound_statement();
        std::shared_ptr<AST> assign_op();
        std::shared_ptr<AST> term();
        std::shared_ptr<AST> factor();
};

#endif