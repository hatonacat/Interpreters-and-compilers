#include "ast_visitor.h"
#include "interpreter.h"
#include "parser.h"

Interpreter::Interpreter(Parser *init_parser) {
    parser = init_parser;
}

void Interpreter::interpret() {
    AST* tree_head_node = parser->parse();
    NodeVisitor visitor;

    tree_head_node->accept(visitor);
}

