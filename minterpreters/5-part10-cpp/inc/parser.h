/**
 * Converts a token stream into an intermediate AST representation 
**/

#ifndef PARSER_H
#define PARSER_H

class AST;
class Lexer;

class Parser {
    public:
        Parser(Lexer *init_lexer);
        ~Parser() {};

        // Convert Token stream into AST and return pointer to head
        AST* parse();
        void parsing_error(std::string err_message);

    private:
        Lexer *lexer = nullptr;

        /*
        * GRAMMARS
        */
        void eat(std::string);
        AST* term();
        AST* factor();
};


/*
 * AST NODES
 */

class AST {};

class BinOp_node : public AST {
    public:
        BinOp_node(AST* init_left, Token init_op, AST* init_right);
    
    private:
        AST* left;
        Token op;
        AST* right;
};

class Integer_node :public AST {
    public:
        Integer_node() {};
        Integer_node(int init_value) {value = init_value;};
        ~Integer_node() {};

        int get_value() {return value;};
        void set_value(int init_value) {value = init_value;}

    private:
        int value;
};

class Real_node :public AST{
    public:
        Real_node() {};
        Real_node(float init_value) {value = init_value;};
        ~Real_node() {};
        
        float get_value() {return value;};
        void set_value(float init_value) {value = init_value;}

    private:
        float value;
};

#endif