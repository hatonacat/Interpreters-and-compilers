#include "lexer.h"
#include "parser.h"
#include "token.h"

Parser::Parser(Lexer *init_lexer) {
    lexer = init_lexer;
}

AST* Parser::parse() {
    Token token;

    AST* node = term();
    // while (token.get_type() != "EOF") {
    //     token = lexer->get_next_token();
    //     std::cout << token << std::endl;
    // }
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

    AST* binop_node = new BinOp_node(node, op, factor());

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
        node = new Integer_node(token_value);
        eat("INTEGER");
    } 
    else if (token.get_type() == "REAL") {
        float token_value = std::stof(token.get_value());
        node = new Real_node(token_value);
        eat("REAL");
    }
    else {
        parsing_error("No matching options found in 'factor' grammar");
    }

    return node;   
}


/*
 * AST NODES
 */
BinOp_node::BinOp_node(AST* init_left, Token init_op, AST* init_right) {
    left = init_left;
    op = init_op;
    right = init_right;
}