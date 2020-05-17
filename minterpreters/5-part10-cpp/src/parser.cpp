#include "ast_visitor.h"
#include "lexer.h"
#include "parser.h"
#include "token.h"

Parser::Parser(Lexer *init_lexer) {
    lexer = init_lexer;
}

AST* Parser::parse() {
    Token token;

    AST* node = term();

    return node;
}

void Parser::parsing_error(std::string err_message) {
    if (err_message == "") {
        std::cout << "Parser error" << std::endl;
    }
    else {
        std::cout << err_message << std::endl;
        exit(EXIT_FAILURE);
    }
}

void Parser::eat(std::string token_type) {
    std::string current_token_type = lexer->get_current_token().get_type();
    if (current_token_type == token_type) {
        lexer->get_next_token();
    }
    else {
        parsing_error("Failed eat request, got: "+ current_token_type + 
                      "expected: " + token_type);
    }
}

/*
* GRAMMARS
*/

AST* Parser::term() {
    /*
     * FACTOR ((MUL|DIV) FACTIR)*
     */
    AST* node = factor();
    Token op = lexer->get_current_token();
    if (op.get_type()=="MUL") {
        eat("MUL");
    }
    else {
        eat("DIV");
    }

    AST* binop_node = new BinOpNode(node, op, factor());

    return binop_node;
}

AST* Parser::factor() {
    /*
    * INTEGER | REAL | LPAREN EXPR RPAREN
    */
    Token token = lexer->get_current_token();
    AST* node;

    if (token.get_type() == "INTEGER") {
        int token_value = std::stoi(token.get_value());
        node = new IntegerNode(token_value);
        eat("INTEGER");
    } 
    else if (token.get_type() == "REAL") {
        float token_value = std::stof(token.get_value());
        node = new RealNode(token_value);
        eat("REAL");
    }
    else {
        parsing_error("No matching options found in 'factor' grammar");
    }

    return node;   
}

