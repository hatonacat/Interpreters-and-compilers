#include "ast_visitor.h"

/**
 * AST structure and nodes
**/

BlockNode::BlockNode(std::shared_ptr<AST> declaration_node, std::shared_ptr<AST> cs_statements) {
    declarations = declaration_node;
    compounds_statements = cs_statements;
}

void CompoundNode::add_statement(std::shared_ptr<AST> statement) {
    statement_list.push_back(statement);
}

AssignNode::AssignNode(std::shared_ptr<AST> init_type, std::shared_ptr<AST> init_variable, std::shared_ptr<AST> init_value) : 
        type_node(init_type), 
        variable_node(init_variable), 
        value_node(init_value) 
        {}

TypeNode::TypeNode(std::string init_type, std::string init_value) {
    type = init_type;
    value = init_value;
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

void BlockNode::accept(Visitor &v) {
    v.visit(this);
}

void DeclarationNode::accept(Visitor &v) {
    v.visit(this);
}

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

void UnaryNode::accept(Visitor &v) {
    v.visit(this);
}

void EmptyNode::accept(Visitor &v) {
    v.visit(this);
}

/**
 * Visitor design pattern
**/
void Visitor::add_integer(Variable<int> var) {
    integer_map.insert(std::pair<std::string, int>(var.get_name(), var.get_value()));
}

void Visitor::add_integer(std::string var_name, int value) {
    integer_map.insert(std::pair<std::string, int>(var_name, value));
}

void Visitor::add_real(Variable<float> var) {
    real_map.insert(std::pair<std::string, float>(var.get_name(), var.get_value()));
}

void Visitor::add_real(std::string var_name, float value) {
    real_map.insert(std::pair<std::string, float>(var_name, value));
}

void Visitor::add_string(std::string var_name, std::string value) {
    string_map.insert(std::pair<std::string, std::string>(var_name, value));
}

void NodeVisitor::visit(BlockNode *node) {
    std::cout << "Visiting Block" << std::endl;
    std::shared_ptr<AST> declaration_node = node->get_declarations();
    std::shared_ptr<AST> cs_node = node->get_compound_statements();     

    if (declaration_node) {declaration_node->accept(*this);};
    cs_node->accept(*this);
};

void NodeVisitor::visit(DeclarationNode *node) {
    std::cout << "Visiting Declarations" << std::endl;
};

void NodeVisitor::visit(CompoundNode *node) {
    std::cout << "Visiting Compound" << std::endl;

    for (auto it: node->get_statements()) {
        it->accept(*this);
    }
};

void NodeVisitor::visit(AssignNode *node) {
    std::cout << "Visiting assign" << std::endl;

    std::shared_ptr<AST> type_node = node->get_type();
    std::shared_ptr<AST> var_node = node->get_variable();
    std::shared_ptr<AST> value_node = node->get_value();

    type_node->accept(*this);
    std::string type = get_running_type();
    var_node->accept(*this);
    std::string name = get_running_var();    
    value_node->accept(*this);

    if (type == "INT") {
        int value = get_running_integer();
        add_integer(Variable<int>(type, name, value));
    }
    else if (type == "REAL") {
        float value = get_running_float();
        add_real(Variable<float>(type, name, value));
    }

};

void NodeVisitor::visit(TypeNode *node) {
    std::cout << "Visiting Type" << std::endl;
    std::string var_type = node->get_value();

    set_running_type(var_type); 
};

void NodeVisitor::visit(VariableNode *node) {
    std::cout << "Visiting variable" << std::endl;
    std::string var_name = node->get_name();

    set_running_var(var_name);
};

void NodeVisitor::visit(BinOpNode *node) {
    std::cout << "Visiting binop" << std::endl;

    std::shared_ptr<AST> left_node = node->get_left();
    std::shared_ptr<AST> right_node = node->get_right();
    std::string op_type = node->get_op().get_type();
    
    if (get_running_type() == "INT") {
        left_node->accept(*this);
        int left = get_running_integer();
        right_node->accept(*this);
        int right = get_running_integer();
        
        set_running_integer(BinOpCalc(left, op_type, right));
        std::cout << "left: " << left << " right: " << right << " op: " << op_type << 
                     " Running int: " << get_running_integer() << std::endl;
    }
    else if (get_running_type() == "REAL") {
        left_node->accept(*this);
        float left = get_running_float();
        right_node->accept(*this);
        float right = get_running_float();
        
        set_running_float(BinOpCalc(left, op_type, right));
        std::cout << "left: " << left << " right: " << right << " op: " << op_type << 
                     " Running float: " << get_running_float() << std::endl;
    }
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
    std::cout << "Real value: " << value << std::endl;

    set_running_float(value);
};

void NodeVisitor::visit(UnaryNode *node) {
    std::cout << "Visiting Unary" << std::endl;

    std::shared_ptr<AST> child_node = node->get_node();
    child_node->accept(*this);

    if (node->get_type() == "MINUS") {
        set_running_integer(-1 * get_running_integer());
        set_running_float(-1 * get_running_float());
    }
};

void NodeVisitor::visit(EmptyNode *node) {
    std::cout << "Visiting empty" << std::endl;
};