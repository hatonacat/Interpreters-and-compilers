from collections import namedtuple
import re

Token = namedtuple('Token', 'type value')

###########################
#   LEXER                 #
###########################

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

###########################
#   PARSER                #
###########################

class Parser:
    '''
    Match a series of tokens to expected structures and
    execute the result of these structures.
    '''
    def __init__(self, lexer):
        self.lexer = lexer
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

    def parse(self):
        return self.expr()

    def parse_error(self, current_token, token_type):
        '''Raise a parse exception'''
        raise Exception(f"Parsing error, Expected: {token_type}, Got: {current_token}")

    # Anticipated structures =========================
    def expr(self):
        '''
        expr: term ((PLUS|MINUS) term)*
        term: factor ((MUL|DIV) factor)*
        factor: (PLUS | MINUS) FACTOR | INTEGER | LPAREN EXPR RPAREN
        ''' 
        node = self.term()

        while (self.current_token.type in ("PLUS", "MINUS")):
            op = self.current_token
            if op.type == "PLUS":
                self.eat("PLUS")
            elif op.type == "MINUS":
                self.eat("MINUS")

            node = BinOp(node, op, self.term())

        return node
    
    def term(self):
        '''
        term: factor ((MUL|DIV) factor)*
        factor: (PLUS | MINUS) FACTOR | INTEGER | LPAREN EXPR RPAREN
        ''' 
        node = self.factor()

        while (self.current_token.type in ("MUL", "DIV")):
            op = self.current_token
            if op.type == "MUL":
                self.eat("MUL")
            elif op.type == "DIV":
                self.eat("DIV")

            node = BinOp(node, op, self.factor())

        return node

    def factor(self):
        '''
        factor: (PLUS | MINUS) FACTOR | INTEGER | LPAREN EXPR RPAREN
        '''
        token = self.current_token
        if self.current_token.type in ["PLUS", "MINUS"]:
            if self.current_token.type == "PLUS":
                self.eat("PLUS")
                return UnaryOp(token, self.factor())
            elif self.current_token.type == "MINUS":
                self.eat("MINUS")
                return UnaryOp(token, self.factor())
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node
        elif token.type == "INTEGER":
            self.eat("INTEGER")
            return Num(token)
        else:
            self.parse_error("NONE", "PLUS|MINUS, INTEGER OR LPAREN")

###########################
#   INTERPRETER           #
###########################

# AST node types, BinOp and Num(ber)
class BinOp:
    def __init__(self, left, op, right):
        '''
        left and right are expected to be Num objects
        op is expected to be a Token.
        '''
        self.left = left
        self.op = op
        self.right = right

class Num:
    def __init__(self, token):
        '''
        Num is a leaf node of the AST structure
        '''
        self.token = token
        self.value = token.value

class UnaryOp:
    def __init__(self, op, child):
        '''
        Unary operator, expects an operation and
        a child node
        '''
        self.op = op
        self.child = child 

# Create generic visitor module
class NodeVisitor:
    def visit(self, node):
        '''
        Produce module name from passed node and return 
        relevant visitor method
        '''
        module_name = 'visitor_' + type(node).__name__
        method = getattr(self, module_name, self.visit_error)
        return method(node)

    def visit_error(self, node):
        raise Exception(f"No method visitor_{type(node).__name__} found")

# Create interpreter visitor actions
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visitor_BinOp(self, node):
        if node.op.type == "PLUS":
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == "MINUS":
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == "MUL":
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == "DIV":
            return self.visit(node.left) / self.visit(node.right)

    def visitor_Num(self, node):
        return node.value

    def visitor_UnaryOp(self, node):
        if node.op.type == "PLUS":
            return self.visit(node.child)
        elif node.op.type == "MINUS":
            return -1 * self.visit(node.child)

    def interpret(self):
        tree = parser.parse()
        return self.visit(tree)
        # return parser.parse()

###########################
#   MAIN                  #
###########################

if __name__ == "__main__":
    #phrase = "2*2"
    while(1):
        phrase = input("> ")
        if phrase in ["q", "quit"]:
            quit()
        elif not phrase:
            continue

        lexer = Lexer(phrase)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)

        result = interpreter.interpret()
        print(f"Result: {result}")

