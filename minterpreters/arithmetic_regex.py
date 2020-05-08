from collections import namedtuple
import re

Token = namedtuple('Token', 'type value')

class Lexer:
    '''
    Returns tokens one at a time based on a dictionary
    of regex expressions.
    '''

    def __init__(self, phrase):
        # A default dictionary of regex phrases
        self.token_codes = {
            "WORD":r"[a-zA-Z]+", 
            "INTEGER":r"\d+",
            "DIV":r"[/]",
            "LPAREN":r"[(]",
            "MINUS":"[-]",
            "MUL":"[*]",
            "PLUS":"[+]",
            "RPAREN":r"[)]"
        }

        self.pattern = self._assemble_regex_pattern()   # Combine regex dictionary
        self.phrase = phrase                            # Phrase to tokenise
        self.pos = 0                                    # Position within phrase

    def _assemble_regex_pattern(self):
        '''
        Assembles a regex pattern with named capture groups based off of
        a dictionary of separate regex patterns.
        '''
        pattern = ""
        for token_code in self.token_codes:
            pattern += "(?P<" + token_code + ">" + self.token_codes[token_code] + ")|"
        return pattern[:-1] # Strip trailing '|'

    def get_next_token(self):
        '''
        Yields tokens from a given string and increments position in string
        '''
        match_result = re.search(self.pattern, self.phrase[self.pos:])
        if match_result != None:
            token = self.tokenise(match_result)
            self.pos += match_result.end()  # Next time carry on from the end of the last match
        else:
            token = Token("EOF", "EOF")

        return token

    def tokenise(self, match_result):
        '''
        Converts a Regex match object to a token
        '''
        matching_group = match_result.lastgroup
        match_value = match_result.group(matching_group)

        if match_value.isdigit():
            token = Token(matching_group, int(match_value))
        else:
            token = Token(matching_group, match_value)           

        return token

class Parser:
    '''
    Match a series of tokens to expected structures and
    execute the result of these structures.
    '''
    def __init__(self, phrase):
        self.lexer = Lexer(phrase)
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        '''
        Checks if current token type is the same as anticipated.
        If so, updates current_token to the next token.
        '''
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.parse_error(self.current_token, token_type)
  
    def parse_error(self, current_token, token_type):
        '''Raise a parse exception'''
        raise Exception(f"Parsing error, Expected: {token_type}, Got: {current_token}")

    # Anticipated structures =========================
    def expr(self):
        '''
        expr: term ((PLUS|MINUS) term)*
        term: factor ((MUL|DIV) factor)*
        factor: INTEGER
        ''' 
        result = self.term()

        while (self.current_token.type in ("PLUS", "MINUS")):
            op = self.current_token
            if op.type == "PLUS":
                self.eat("PLUS")
                result += self.term()
            elif op.type == "MINUS":
                self.eat("MINUS")
                result -= self.term()       

        return result
    
    def term(self):
        '''
        term: factor ((MUL|DIV) factor)*
        factor: INTEGER
        ''' 
        result = self.factor()

        while (self.current_token.type in ("MUL", "DIV")):
            op = self.current_token
            if op.type == "MUL":
                self.eat("MUL")
                result *= self.factor()
            elif op.type == "DIV":
                self.eat("DIV")
                result /= self.factor()

        return result

    def factor(self):
        '''
        factor: INTEGER | LPAREN EXPR RPAREN
        '''
        result = self.current_token
        if result.type == "LPAREN":
            self.eat("LPAREN")
            result = self.expr()
            self.eat("RPAREN")
        elif result.type == "INTEGER":
            result = self.current_token.value
            self.eat("INTEGER")
        else:
            self.parse_error("NONE", "INTEGER OR LPAREN")

        return result

if __name__ == "__main__":
    #phrase = "2*2"
    while(1):
        phrase = input("> ")
        if phrase in ["q", "quit"]:
            quit()
        elif not phrase:
            continue

        parser = Parser(phrase)
        result = parser.expr()
        print(result)

