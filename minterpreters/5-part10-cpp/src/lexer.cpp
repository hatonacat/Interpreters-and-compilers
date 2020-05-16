#include <iostream>
#include <regex>

#include "lexer.h"

// CONSTRUCTORS AND DESTRUCTORS

Lexer::Lexer(std::string user_code) {
    set_code(user_code);
    pos = 0;
    regex_expressions = {
        {R"([A-Za-z])", "WORD"},
        {R"(\d)", "INTEGER"},
        {R"(\+)", "PLUS"},
        {R"(-)", "MINUS"},
        {R"(\*)", "MUL"},
        {R"(/)", "DIV"},
    };
    current_token = get_next_token();
}

// SETTERS AND GETTERS

std::string Lexer::get_code() {
    if (code=="") {
        return "No input code provided";
    }
    else {
        return code;
    }
}

//CORE FUNCTIONALITY

Token Lexer::get_next_token() {
    Token token;
    if (pos<=code.length()-1) {
        token = tokenise();
    }
    else {
        token = Token("EOF", "EOF");
    }
    std::cout << token << std::endl;
    current_token = token;
    return token;
}

Token Lexer::tokenise() {
    /*
     * Try to match the current code position to any of the expressions in 
     * the regular_expression dictionary.
    */
    std::smatch match_result;
    std::string remaining_code = code.substr(pos);

    for (const auto &expression : regex_expressions) {
        std::regex regex("^" + expression.first); 
        bool regex_result = std::regex_search(remaining_code, match_result, regex);
        
        if (regex_result) {
            pos += match_result[0].length();
            return Token(expression.second, match_result[0]);
        }
    }    
    lexer_error("No matching token found");
}

void Lexer::lexer_error(std::string err_message) {
    if (err_message == "") {
        std::cout << "Lexer error" << std::endl;
    }
    else {
        std::cout << err_message << std::endl;
        exit(EXIT_FAILURE);
    }
}

