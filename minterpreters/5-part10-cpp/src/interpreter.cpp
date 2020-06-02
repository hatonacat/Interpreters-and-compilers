#include "ast_visitor.h"
#include "interpreter.h"
#include "parser.h"
#include "utils.h"

Interpreter::Interpreter(std::string user_code) {
    parser = new Parser(user_code);
}

void Interpreter::interpret() {
    std::shared_ptr<AST> tree_head_node = parser->parse();
    std::cout << "\nParsing complete\n" << std::endl;

    // We want this visitor to return a map of variables
    NodeVisitor top_visitor;
    tree_head_node->accept(top_visitor);
    std::cout << "\nInterpreting complete\n" << std::endl;
    
    std::cout << "Integers: " << std::endl;
    print_map(*top_visitor.get_integer_map());    
    std::cout << "\nFloats: " << std::endl;
    print_map(*top_visitor.get_real_map());   
}

