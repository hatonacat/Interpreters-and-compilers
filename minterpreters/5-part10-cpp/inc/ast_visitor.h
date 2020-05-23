/**
 * The components of an AST tree and the means to visit them
**/

#ifndef AST_H
#define AST_H

#include <map>
#include <memory>

#include "token.h"

/**
 * AST Data structures
**/
class Variable {
    public:
        Variable(std::string init_type, std::string init_name, int init_value);
        ~Variable() {};

        std::string get_type() {return type;};
        std::string get_name() {return name;};
        int get_value() {return value;};
    
    private:
        std::string type;
        std::string name;
        int value;
};

/**
 * AST NODES
**/

class AST {
    public:
        virtual void accept(class Visitor &v) = 0;
};

class AssignNode: public AST {
    public:
        AssignNode(std::shared_ptr<AST> init_type, std::shared_ptr<AST> init_variable, std::shared_ptr<AST> init_value);
        ~AssignNode() {};

        void accept(Visitor &v);

        std::shared_ptr<AST> get_type() {return type_node;};
        std::shared_ptr<AST> get_variable() {return variable_node;};
        std::shared_ptr<AST> get_value() {return value_node;};

    private:
        std::shared_ptr<AST> type_node;
        std::shared_ptr<AST> variable_node;
        std::shared_ptr<AST> value_node;
};

class TypeNode: public AST {
    public:
        TypeNode() {};
        TypeNode(std::string init_type);
        ~TypeNode() {};

        void accept(Visitor &v);

        std::string get_type() {return type;};

    private:
        std::string type;
};

class VariableNode: public AST {
    public:
        VariableNode() {};
        VariableNode(Token init_token);
        ~VariableNode() {};

        void accept(Visitor &v);

        std::string get_name() {return name;};

    private:
        Token token;
        std::string name;
};

class BinOpNode : public AST {
    public:
        BinOpNode(std::shared_ptr<AST> init_left, Token init_op, std::shared_ptr<AST> init_right);

        void accept(Visitor &v);
    
        std::shared_ptr<AST> get_left() {return left;};
        Token get_op() {return op;};
        std::shared_ptr<AST> get_right() {return right;};

    private:
        std::shared_ptr<AST> left;
        Token op;
        std::shared_ptr<AST> right;
};

class IntegerNode :public AST {
    public:
        IntegerNode() {};
        IntegerNode(int init_value) {value = init_value;};
        ~IntegerNode() {};

        void accept(Visitor &v);

        int get_value() {return value;};
        void set_value(int init_value) {value = init_value;}

    private:
        int value;
};

class RealNode :public AST{
    public:
        RealNode() {};
        RealNode(float init_value) {value = init_value;};
        ~RealNode() {};

        void accept(Visitor &v);

        float get_value() {return value;};
        void set_value(float init_value) {value = init_value;}

    private:
        float value;
};

/**
 * Visitor design pattern
**/
class Visitor {
    private:
        std::map<std::string, int> integer_map;
        std::map<std::string, float> float_map;
        std::map<std::string, std::string> string_map;
        int running_integer;
        std::string running_var;

    public:
        virtual void visit(AssignNode *e)=0;
        virtual void visit(TypeNode *e)=0;
        virtual void visit(VariableNode *e)=0;
        virtual void visit(BinOpNode *e)=0;
        virtual void visit(IntegerNode *e)=0;
        virtual void visit(RealNode *e)=0;

        auto get_integer_map() {return &integer_map;};
        auto get_float_map() {return &float_map;};
        auto get_string_map() {return &string_map;};

        void set_running_integer(int value) {running_integer = value;};
        int get_running_integer() {return running_integer;};

        void set_running_var(std::string var) {running_var = var;};
        std::string get_running_var() {return running_var;};

        void add_integer(Variable new_var);
        void add_integer(std::string var_name, int value);
};  

class NodeVisitor : public Visitor {
    private:
        void visit(AssignNode *e);
        void visit(TypeNode *e);
        void visit(VariableNode *e);
        void visit(BinOpNode *e);
        void visit(IntegerNode *e);
        void visit(RealNode *e);
};

#endif