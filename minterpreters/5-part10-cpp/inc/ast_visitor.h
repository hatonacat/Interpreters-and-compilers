/**
 * The components of an AST tree and the means to visit them
**/

#ifndef AST_H
#define AST_H

#include <map>

#include "token.h"

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

class Variable: public AST {
    public:
        Variable() {};
        Variable(Token init_token);
        ~Variable() {};

        void accept(Visitor &v);

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
    public:
        virtual void visit(AssignNode *e)=0;
        virtual void visit(Variable *e)=0;
        virtual void visit(BinOpNode *e)=0;
        virtual int visit(IntegerNode *e)=0;
        virtual void visit(RealNode *e)=0;
};  

class NodeVisitor : public Visitor {
    private:
        void visit(AssignNode *e);
        void visit(Variable *e);
        void visit(BinOpNode *e);
        int visit(IntegerNode *e);
        void visit(RealNode *e);

    public:
        std::map<std::string, int> integers;
        std::map<std::string, float> floats;
        std::map<std::string, std::string> strings;
        int running_integer;
};

#endif