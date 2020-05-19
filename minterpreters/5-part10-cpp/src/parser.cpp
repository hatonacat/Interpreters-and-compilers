#include "ast_visitor.h"
#include "lexer.h"
#include "parser.h"
#include "token.h"

Parser::Parser(std::string user_code) {
    lexer = new Lexer(user_code);
}

Parser::~Parser() {};

AST* Parser::parse() {
    Token token = lexer->get_current_token();
    AST* node = assign_op();

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
                      " expected: " + token_type);
    }
}

/*
* GRAMMARS
*/

AST* Parser::assign_op() {
    /*
    * TYPE VARIABLE EQUALS EXPR
    */
    Token type_token = lexer->get_current_token();
    AST* type_node = new Variable(type_token);
    eat("INT_TYPE");

    Token var_token = lexer->get_current_token();
    AST* var_node = new Variable(var_token);
    eat("VARIABLE");

    eat("EQUALS");

    AST* value_node = term();

    AST* assign_node = new AssignNode(type_node, var_node, value_node);
    return assign_node;
}

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
        std::cout << "Token is: " << token << std::endl;
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

