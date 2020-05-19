/**
 * Walks through an AST tree and evaluates 
**/

#ifndef INTERPRETER_H
#define INTERPRETER_H

#include <map>

class Parser;

class Interpreter {
    public:
        Interpreter(std::string user_code);
        ~Interpreter() {};

        void interpret();
        std::map<std::string, int> var_ints;

    private:
        Parser *parser;
        std::map<std::string, int> integers;
        std::map<std::string, float> floats;
        std::map<std::string, std::string> strings;
};

#endif