#include "ast_visitor.h"

/**
 * AST structure and nodes
**/

void CompoundNode::add_statement(std::shared_ptr<AST> statement) {
    statement_list.push_back(statement);
}

AssignNode::AssignNode(std::shared_ptr<AST> init_type, std::shared_ptr<AST> init_variable, std::shared_ptr<AST> init_value) : 
        type_node(init_type), 
        variable_node(init_variable), 
        value_node(init_value) 
        {}

TypeNode::TypeNode(std::string init_type) {
    type = init_type;
}

VariableNode::VariableNode(Token init_token) {
    token = init_token; 
    name = init_token.get_value();
}

BinOpNode::BinOpNode(std::shared_ptr<AST> init_left, Token init_op, std::shared_ptr<AST> init_right) {
    left = init_left;
    op = init_op;
    right = init_right;
}

/**
 * Accept methods
**/

void CompoundNode::accept(Visitor &v) {
    v.visit(this);
}

void AssignNode::accept(Visitor &v) {
    v.visit(this);
}

void TypeNode::accept(Visitor &v) {
    v.visit(this);   
}

void VariableNode::accept(Visitor &v) {
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

void EmptyNode::accept(Visitor &v) {
    v.visit(this);
}

/**
 * Visitor design pattern
**/
void Visitor::add_integer(Variable var) {
    integer_map.insert(std::pair<std::string, int>(var.get_name(), var.get_value()));
}

void Visitor::add_integer(std::string var_name, int value) {
    integer_map.insert(std::pair<std::string, int>(var_name, value));
}

void NodeVisitor::visit(CompoundNode *node) {
    std::cout << "Visiting Block" << std::endl;

    for (auto it: node->get_statements()) {
        it->accept(*this);
    }
};

void NodeVisitor::visit(AssignNode *node) {
    std::cout << "Visiting assign" << std::endl;

    std::shared_ptr<AST> type_node = node->get_type();
    type_node->accept(*this);
    std::string type = get_running_var();

    std::shared_ptr<AST> var_node = node->get_variable();
    var_node->accept(*this);
    std::string name = get_running_var();    

    std::shared_ptr<AST> value_node = node->get_value();
    value_node->accept(*this);
    int value = get_running_integer();

    add_integer(Variable(type, name, value));
};

void NodeVisitor::visit(TypeNode *node) {
    std::cout << "Visiting Type" << std::endl;
    std::string var_type = node->get_type();

    set_running_var(var_type); 
};

void NodeVisitor::visit(VariableNode *node) {
    std::cout << "Visiting variable" << std::endl;
    std::string var_name = node->get_name();

    set_running_var(var_name);
};

void NodeVisitor::visit(BinOpNode *node) {
    std::cout << "Visiting binop" << std::endl;

    std::shared_ptr<AST> left_node = node->get_left();
    left_node->accept(*this);
    int left = get_running_integer();

    std::shared_ptr<AST> right_node = node->get_right();
    right_node->accept(*this);
    int right = get_running_integer();

    int total;
    std::string op_type = node->get_op().get_type();
    if (op_type == "MUL") {
        total = left * right;
    }
    else if (op_type == "DIV") {
        total = left / right;
    }
    else if (op_type == "PLUS") {
        total = left + right;
    }
    else if (op_type == "MINUS") {
        total = left - right;
    }
    else {
        std::cout << "No valid binary operation found" << std::endl;
    }

    set_running_integer(total);
    std::cout << "left: " << left << " right: " << right << " op: " << op_type << 
                 " Running int: " << get_running_integer() << std::endl;
};

void NodeVisitor::visit(IntegerNode *node) {
    std::cout << "Visiting integer" << std::endl;
    int value = node->get_value();
    std::cout << "Integer value: " << value << std::endl;  
      
    set_running_integer(value);
};

void NodeVisitor::visit(RealNode *node) {
    std::cout << "Visiting real" << std::endl;
    float value = node->get_value();
    std::cout << node->get_value() << std::endl;

    //return value;
};

void NodeVisitor::visit(EmptyNode *node) {
    std::cout << "Visiting empty" << std::endl;
};

Variable::Variable(std::string init_type, std::string init_name, int init_value) {
    type = init_type;
    name = init_name;
    value = init_value;
}