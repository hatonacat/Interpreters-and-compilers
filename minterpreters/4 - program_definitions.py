from collections import namedtuple
from decorators import function_details
import re

Token = namedtuple('Token', 'type value')

RESERVED_KEYWORDS = {
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
}

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
            "DIV":          r"div",
            "ID":           r"[a-zA-Z_][a-zA-Z0-9]*", 
            "INTEGER":      r"\d+",
            "LPAREN":       r"[(]",
            "MINUS":        r"[-]",
            "MUL":          r"[*]",
            "PLUS":         r"[+]",
            "RPAREN":       r"[)]",
            "ASSIGN":       r":=",
            "SEMI":         r";",
            "DOT":          r"\.",
        }

        self.pattern = self._assemble_regex_pattern()   # Combine regex dictionary
        self.phrase = phrase.rstrip()                   # Phrase to tokenise, strip trailing whitespace
        self.pos = 0                                    # Position within phrase

    def _assemble_regex_pattern(self):
        '''
        Assembles a regex pattern with named capture groups based off of
        a dictionary of separate regex patterns.
        '''
        # Pattern prefix, find match at start of string, excluding whitespace, start non-capture group
        pattern = r"^\s*(?:" 

        # Assemble the regex functions in the token_codes dict into one long "or'd" list
        for token_code in self.token_codes:
            pattern += "(?P<" + token_code + ">" + self.token_codes[token_code] + ")|"

        # Strip trailing '|' and terminate
        pattern = pattern[:-1] + ")" 
        return pattern 

    def get_next_token(self):
        '''
        Yields tokens from a given string and increments position in string
        '''
        if self.pos == len(self.phrase):
            token = Token("EOF", "EOF")
        else:
            # Not at end of phrase, expecting a valid character
            match_result = re.search(self.pattern, self.phrase[self.pos:])
            if match_result != None:
                token = self.tokenise(match_result)
                self.pos += match_result.end()  # Next time carry on from the end of the last match
            else:
                raise Exception("Parsing error, no valid characters found")

        print(f"Next token: {token}")
        return token

    def tokenise(self, match_result):
        '''
        Converts a Regex match object to a token
        '''
        matching_group = match_result.lastgroup
        match_value = match_result.group(matching_group)

        if matching_group == 'ID':
            # Check if standard keyword
            token = RESERVED_KEYWORDS.get(match_value.upper(), Token(matching_group, match_value))
        elif match_value.isdigit():
            # Integers stored as int rather than string
            token = Token(matching_group, int(match_value))
        else:
            token = Token(matching_group, match_value)           

        return token

###########################
#   AST                   #
###########################

# AST nodes ========================================
class Assign:
    '''
    left = right
    left is a var node
    right is a expr node
    '''
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Compound:
    '''
    Represents a BEGIN...END block
    '''
    def __init__(self):
        self.children = []

class NoOp:
    '''
    A valid empty statement
    '''
    pass

class Var:
    '''
    A variable - Constructed from an ID node
    '''
    def __init__(self, token):
        self.token = token
        self.value = token.value

# AST nodes - Arithmetic ============================
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
        print(f"visit request for: {node}")
        module_name = 'visitor_' + type(node).__name__
        method = getattr(self, module_name, self.visit_error)
        return method(node)

    def visit_error(self, node):
        raise Exception(f"No method visitor_{type(node).__name__} found")

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
            print(f"Eating token type: {token_type}")
            self.current_token = self.lexer.get_next_token()
        else:
            self.parse_error()

    def parse(self):
        node = self.program()
        if self.current_token.type != "EOF":
            return self.parse_error()

        return node

    def parse_error(self):
        '''Raise a parse exception'''
        raise Exception(f"Parsing error")

    # GRAMMARS =========================
    @function_details
    def program(self):
        '''
        compound statement DOT
        '''
        node = self.compound_statement()
        self.eat("DOT")
        return node

    @function_details  
    def compound_statement(self):
        '''
        BEGIN statement_list END
        '''
        self.eat("BEGIN")
        nodes = self.statement_list()
        self.eat("END")

        root = Compound()
        for node in nodes:
            root.children.append(node)
            print(f"root.children is now: {root.children}")

        print(f"root: {root}")
        print(f"root children: {root.children}")
        return root

    @function_details
    def statement_list(self):
        '''
        statement | statement SEMI statement_list
        '''
        node = self.statement()
        results = [node]
        print(f"statement list results (pre): {results}")

        while self.current_token.type == "SEMI":
            self.eat("SEMI")
            results.append(self.statement())

        if self.current_token.type == "ID":
            self.parse_error()

        print(f"statement list results: {results}")
        return results        

    @function_details   
    def statement(self):
        '''
        compound statement | assignment_statement | empty
        '''
        token = self.current_token
        if token.type == "BEGIN":
            node = self.compound_statement()
        elif token.type == "ID":
            node = self.assignment_statement()
        else:
            node = self.empty()

        return node

    @function_details  
    def assignment_statement(self):
        '''
        assignment_statement : variable ASSIGN expr
        '''
        left = self.variable()
        op_token = self.current_token
        self.eat("ASSIGN")
        right = self.expr()
        node = Assign(left, op_token, right)

        return node

    @function_details    
    def variable(self):
        '''
        variable : ID
        '''
        node = Var(self.current_token)
        self.eat("ID")

        return node

    @function_details    
    def empty(self):
        '''Empty : '''
        return NoOp()

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
        factor: (PLUS | MINUS) FACTOR | INTEGER | LPAREN EXPR RPAREN | VAR
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
            node = self.variable()
            return node

###########################
#   INTERPRETER           #
###########################

# Create interpreter visitor actions
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visitor_Assign(self, node):
        var_name = node.left.value.upper()
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visitor_BinOp(self, node):
        if node.op.type == "PLUS":
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == "MINUS":
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == "MUL":
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == "DIV":
            return self.visit(node.left) / self.visit(node.right)

    def visitor_Compound(self, node):
        print(f"visiting children of: {node}")
        print(f"Node children: {node.children}")
        for child in node.children:
            print(f"Visiting child: {child}")
            self.visit(child)

    def visitor_NoOp(self, node):
        print(f"visiting no-op")
        pass

    def visitor_Num(self, node):
        return node.value

    def visitor_UnaryOp(self, node):
        if node.op.type == "PLUS":
            return self.visit(node.child)
        elif node.op.type == "MINUS":
            return -1 * self.visit(node.child)

    def visitor_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name.upper())
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def interpret(self):
        tree = self.parser.parse()
        print(f"Root of tree: {tree}")
        return self.visit(tree)

###########################
#   MAIN                  #
###########################

if __name__ == "__main__":
    #phrase = "2*2"
    while(1):
        phrase = input("> ")
        if phrase in ["q", "quit"]:
            quit()
        # elif not phrase:
        #     continue

        phrase = """
            BEGIN

                BEGIN
                    number := 2;
                    a := NumBer;
                    B := 10 * a + 10 * NUMBER div 4;
                    c := a - - b
                end;

                x := 11;
            END."""

        print(f"phrase: {phrase}")
        lexer = Lexer(phrase)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()
        print(interpreter.GLOBAL_SCOPE)


"""
            BEGIN 
                BEGIN 
                    _number:=2; 
                    a:=_number; 
                    b := 10*a + 10*_number / 4; 
                    c := a - - b; 
                END;  
                x:= 11; 
            END ."""
