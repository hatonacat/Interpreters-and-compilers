#include "ast_visitor.h"

/**
 * AST structure and nodes
**/

AssignNode::AssignNode(AST* init_type, AST* init_variable, AST* init_value) {
    type = init_type;
    variable = init_variable;
    value = init_value;
}

VariableNode::VariableNode(Token init_token) {
    token = init_token; 
    name = init_token.get_value();
}

BinOpNode::BinOpNode(AST* init_left, Token init_op, AST* init_right) {
    left = init_left;
    op = init_op;
    right = init_right;
}

void AssignNode::accept(Visitor &v) {
    Variable new_var = v.visit(this);
    v.add_integer(new_var);
}

void VariableNode::accept(Visitor &v) {
    std::string var_name = v.visit(this);
    v.set_running_var(var_name);
}

void BinOpNode::accept(Visitor &v) {
    int value = v.visit(this);
    v.set_running_integer(value);
}

void IntegerNode::accept(Visitor &v) {
    int value = v.visit(this);
    v.set_running_integer(value);
}

void RealNode::accept(Visitor &v) {
    v.visit(this);
}

/**
 * Visitor design pattern
**/
void Visitor::add_integer(Variable var) {
    integers.insert(std::pair<std::string, int>(var.get_name(), var.get_value()));
}

void Visitor::add_integer(std::string var_name, int value) {
    integers.insert(std::pair<std::string, int>(var_name, value));
}

Variable NodeVisitor::visit(AssignNode *node) {
    std::cout << "Visiting assign" << std::endl;
    NodeVisitor visitor;    
    
    AST *var_node = node->get_variable();
    var_node->accept(visitor);
    std::string name = visitor.get_running_var();    

    AST *value_node = node->get_value();
    value_node->accept(visitor);
    int value = visitor.get_running_integer();

    return Variable(name, value);
};

std::string NodeVisitor::visit(VariableNode *node) {
    std::cout << "Visiting variable" << std::endl;
    std::string var_name = node->get_name();
    return var_name;
};

int NodeVisitor::visit(BinOpNode *node) {
    std::cout << "Visiting binop" << std::endl;
    NodeVisitor visitor;

    AST *left_node = node->get_left();
    left_node->accept(visitor);
    int left = visitor.get_running_integer();

    AST *right_node = node->get_right();
    right_node->accept(visitor);
    int right = visitor.get_running_integer();

    int total;
    if (node->get_op().get_type() == "MUL") {
        total = left*right;
    }
    else {
        std::cout << "No valid binary operation found" << std::endl;
    }

    return total;
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

Variable::Variable(std::string init_var_name, int init_value) {
    var_name = init_var_name;
    value = init_value;
}