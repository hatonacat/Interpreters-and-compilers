/**
 * Walks through an AST tree and evaluates 
**/

#ifndef INTERPRETER_H
#define INTERPRETER_H

#include <map>

class Parser;

class Interpreter {
    public:
        Interpreter(Parser *init_parser);
        ~Interpreter() {};

        void interpret();
        std::map<std::string, int> var_ints;

    private:
        Parser *parser;

};

#endif