#include <memory>

#include "ast_visitor.h"
#include "lexer.h"
#include "parser.h"
#include "token.h"

Parser::Parser(std::string user_code) : lexer(std::make_unique<Lexer>(user_code)) {}

Parser::~Parser() {};

std::shared_ptr<AST> Parser::parse() {
    Token token = lexer->get_current_token();
    std::shared_ptr<AST> node = compound_statement();

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

std::shared_ptr<AST> Parser::compound_statement() {
    /*
     * BEGIN STATEMENT_LIST END
    */
    eat("BEGIN");

    std::shared_ptr<AST> node;
    node = statement_list();

    eat("END");
    return node;

}

std::shared_ptr<AST> Parser::statement_list() {
    /*
     * STATEMENT*
    */
    std::unique_ptr<BlockNode> node = std::make_unique<BlockNode>();
    
    node->add_statement( statement() );
    while (lexer->get_current_token().get_type() != "END") {
        node->add_statement( statement() );
    }

    return node;
}

std::shared_ptr<AST> Parser::statement() {
    /*
     * (COMPOUND STATEMENT | ASSIGN_OP | EMPTY) SEMI
    */
    std::shared_ptr<AST> node;
    std::string node_type = lexer->get_current_token().get_type();

    if (node_type == "TYPE") {node = assign_op();}
    else if (node_type == "BEGIN") {node = compound_statement();}
    else {node = empty();}

    eat("SEMI");

    return node;
}

std::shared_ptr<AST> Parser::assign_op() {
    /*
    * TYPE VARIABLE EQUALS EXPR
    */
    // TYPE
    Token type_token = lexer->get_current_token();
    std::shared_ptr<AST> type_node = std::make_shared<TypeNode>(type_token.get_type());
    eat("TYPE");

    // VARIABLE
    Token var_token = lexer->get_current_token();
    std::shared_ptr<AST> var_node = std::make_shared<VariableNode>(var_token);
    eat("VARIABLE");
    eat("EQUALS");

    // EXPR
    std::shared_ptr<AST> value_node (expr());

    std::shared_ptr<AST> assign_node = std::make_shared<AssignNode>(type_node, var_node, value_node);
    return assign_node;
}

std::shared_ptr<AST> Parser::expr() {
    /*
    * TERM ((PLUS|MINUS) TERM)*
    */   
    std::shared_ptr<AST> node (term());

    Token op = lexer->get_current_token();
    while((op.get_type() == "PLUS") || op.get_type() == "MINUS" ) {
        if (op.get_type()=="PLUS") { eat("PLUS"); }
        else { eat("MINUS"); }

        node = std::make_shared<BinOpNode>(BinOpNode(node, op, term()));
        op = lexer->get_current_token();
    }

    return node;
}

std::shared_ptr<AST> Parser::term() {
    /*
     * FACTOR ((MUL|DIV) FACTOR)*
     */
    std::shared_ptr<AST> node (factor());

    Token op = lexer->get_current_token();
    while((op.get_type() == "MUL") || op.get_type() == "DIV" ) {
        if (op.get_type()=="MUL") {
            eat("MUL");
        }
        else {
            eat("DIV");
        }

        node = std::make_shared<BinOpNode>(BinOpNode(node, op, factor()));
        op = lexer->get_current_token();
    }

    return node;
}

std::shared_ptr<AST> Parser::factor() {
    /*
    * INTEGER | REAL | LPAREN EXPR RPAREN
    */
    Token token = lexer->get_current_token();
    std::shared_ptr<AST> node;

    if (token.get_type() == "INTEGER") {
        int token_value = std::stoi(token.get_value());
        node = std::make_shared<IntegerNode>(IntegerNode(token_value));
        eat("INTEGER");
    } 
    else if (token.get_type() == "REAL") {
        float token_value = std::stof(token.get_value());
        node = std::make_shared<RealNode>(RealNode(token_value));
        eat("REAL");
    }
    else if (token.get_type() == "LPAREN") {
        eat("LPAREN");
        node = expr();
        eat("RPAREN");
    }
    else {
        parsing_error("No matching options found in 'factor' grammar");
    }

    return node;   
}

std::shared_ptr<AST> Parser::empty() {
    std::shared_ptr<EmptyNode> node = std::make_shared<EmptyNode>(EmptyNode());

    return node;
}