#include "ast_visitor.h"

/**
 * AST structure and nodes
**/

AssignNode::AssignNode(AST* init_type, AST* init_variable, AST* init_value) {
    type = init_type;
    variable = init_variable;
    value = init_value;
}

Variable::Variable(Token init_token) {
    token = init_token; name = init_token.get_value();
}

BinOpNode::BinOpNode(AST* init_left, Token init_op, AST* init_right) {
    left = init_left;
    op = init_op;
    right = init_right;
}

void AssignNode::accept(Visitor &v) {
    v.visit(this);
}

void Variable::accept(Visitor &v) {
    v.visit(this);
}

void BinOpNode::accept(Visitor &v) {
    v.visit(this);
}

void IntegerNode::accept(Visitor &v) {
    v.visit(this);
}

void RealNode::accept(Visitor &v) {
    v.visit(this);
}

/**
 * Visitor design pattern
**/
void NodeVisitor::visit(AssignNode *node) {
    std::cout << "Visiting assign" << std::endl;
    NodeVisitor visitor;    
    
    AST *var_node = node->get_variable();
    var_node->accept(visitor);

    AST *value_node = node->get_value();
    value_node->accept(visitor);
};

void NodeVisitor::visit(Variable *node) {
    std::cout << "Visiting variable" << std::endl;
};

void NodeVisitor::visit(BinOpNode *node) {
    std::cout << "Visiting binop" << std::endl;
    NodeVisitor visitor;

    AST *left_node = node->get_left();
    left_node->accept(visitor);

    AST *right_node = node->get_right();
    right_node->accept(visitor);
};

int NodeVisitor::visit(IntegerNode *node) {
    std::cout << "Visiting integer" << std::endl;
    int value = node->get_value();
    std::cout << "Integer value: " << value << std::endl;  
      
    return value;
};

void NodeVisitor::visit(RealNode *node) {
    std::cout << "Visiting real" << std::endl;
    std::cout << node->get_value() << std::endl;
};