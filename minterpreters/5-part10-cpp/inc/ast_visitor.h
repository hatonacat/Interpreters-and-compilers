/**
 * The components of an AST tree and the means to visit them
**/

#ifndef AST_H
#define AST_H

#include <map>

#include "token.h"

/**
 * AST Data structures
**/
class Variable {
    public:
        Variable(std::string init_var_name, int init_value);
        ~Variable() {};

        std::string get_name() {return var_name;};
        int get_value() {return value;};
    
    private:
        std::string var_name;
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
        AssignNode() {};
        AssignNode(AST* init_type, AST* init_variable, AST* init_value);
        ~AssignNode() {};

        void accept(Visitor &v);

        AST* get_type() {return type;};
        AST* get_variable() {return variable;};
        AST* get_value() {return value;};

    private:
        AST* type;
        AST* variable;
        AST* value;
};

// class BeginNode: public AST {
//     public:
//         BeginNode(Token init_token) {token = init_token; type = init_token.get_type();};
//         ~BeginNode() {};

//     private:
//         Token token;
//         std::string type;
// };

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
        BinOpNode(AST* init_left, Token init_op, AST* init_right);

        void accept(Visitor &v);
    
        AST *get_left() {return left;};
        Token get_op() {return op;};
        AST *get_right() {return right;};

    private:
        AST* left;
        Token op;
        AST* right;
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
        std::map<std::string, int> integers;
        std::map<std::string, float> floats;
        std::map<std::string, std::string> strings;
        int running_integer;
        std::string running_var;

    public:
        virtual Variable visit(AssignNode *e)=0;
        virtual std::string visit(VariableNode *e)=0;
        virtual int visit(BinOpNode *e)=0;
        virtual int visit(IntegerNode *e)=0;
        virtual void visit(RealNode *e)=0;

        void set_running_integer(int value) {running_integer = value;};
        int get_running_integer() {return running_integer;};

        void set_running_var(std::string var) {running_var = var;};
        std::string get_running_var() {return running_var;};

        void add_integer(Variable new_var);
        void add_integer(std::string var_name, int value);

        void print_integers() {
            std::cout << "Printing map:" << std::endl;
            for (auto it: integers) {
                std::cout << "Quack" << std::endl;
                std::cout << it.first << " = " << it.second << std::endl;
            }
        }
};  

class NodeVisitor : public Visitor {
    private:
        Variable visit(AssignNode *e);
        std::string visit(VariableNode *e);
        int visit(BinOpNode *e);
        int visit(IntegerNode *e);
        void visit(RealNode *e);
};

#endif