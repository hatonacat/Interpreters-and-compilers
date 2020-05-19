#include <iostream>
#include <regex>

#include "lexer.h"

// CONSTRUCTORS AND DESTRUCTORS

Lexer::Lexer(std::string user_code) {
    set_code(user_code);
    pos = 0;
    regex_expressions = {
        {R"(\d)", "INTEGER"},
        {R"(\+)", "PLUS"},
        {R"(-)", "MINUS"},
        {R"(\*)", "MUL"},
        {R"(/)", "DIV"},
        {R"(=)", "EQUALS"},
        {R"([A-Za-z][A-Za-z0-9]*)", "VARIABLE"},
        {R"(\s+)", "WHITESPACE"},
    };
    protected_terms = {
        {"int", "INT_TYPE"},
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

std::string Lexer::protected_check(std::string matching_phrase) {
    // Returns the protected values if found, otherwise reutnrs "Not protected"
    std::cout << "Checking: " << matching_phrase << std::endl;
    auto protected_lookup = protected_terms.find(matching_phrase);
    if (protected_lookup == protected_terms.end()) {
        return "Not protected";
    }
    else {
        return protected_lookup->second;       
    }
}

Token Lexer::get_next_token() {
    Token token;
    if (pos<=code.length()-1) {
        token = tokenise();
    }
    else {
        token = Token("EOF", "EOF");
    }

    current_token = token;
    std::cout << token << std::endl;
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
        remaining_code = code.substr(pos);
        std::regex regex("^" + expression.first); 
        bool regex_result = std::regex_search(remaining_code, match_result, regex);

        Token token;
        if (regex_result) {
            std::string matching_phrase = match_result[0];
            pos += matching_phrase.length();
            
            if (expression.second == "WHITESPACE") {
                token = tokenise();               
            }
            else if (expression.second == "VARIABLE") {
                std::string protected_type = protected_check(matching_phrase);
                if (protected_type == "Not protected") {
                    token = Token(expression.second, matching_phrase);                    
                }
                else {token = Token(protected_type, matching_phrase);}
            }
            else {token = Token(expression.second, matching_phrase);}

            return token;
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

