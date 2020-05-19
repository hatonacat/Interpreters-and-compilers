#include "ast_visitor.h"
#include "interpreter.h"
#include "parser.h"

Interpreter::Interpreter(std::string user_code) {
    parser = new Parser(user_code);
}

void Interpreter::interpret() {
    AST* tree_head_node = parser->parse();
    std::cout << "\nParsing complete\n" << std::endl;

    // We want this visitor to return a map of variables
    NodeVisitor top_visitor;
    tree_head_node->accept(top_visitor);
    std::cout << "\nInterpreting complete\n" << std::endl;
}

