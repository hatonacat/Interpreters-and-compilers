###############################################################################
#                                                                             #
#  DATA STRUCTURES & PROGRAM INFO                                             #
#                                                                             #
###############################################################################


BEGIN           = "BEGIN"
COLON           = "COLON"
COMMA           = "COMMA"
DOT             = "DOT"
EOF             = "EOF"
EQUALS          = "EQUALS"
END             = "END"
FLOAT_DIV       = "FLOAT DIV"
ID              = "ID"
INTEGER         = "INTEGER"
INTEGER_CONST   = "INTEGER_CONST"
INTEGER_DIV     = "INTEGER_DIV"
LPAREN          = "LPAREN"
MINUS           = "MINUS"
MUL             = "MUL"
PLUS            = "PLUS"
PROCEDURE       = "PROCEDURE"
PROGRAM         = "PROGRAM"
RPAREN          = "RPAREN"
REAL            = "REAL"
REAL_CONST      = "REAL_CONST"
SEMI            = "SEMI"
VAR             = "VAR"
VARIABLE        = "VARIABLE"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        #print(self)

    def __str__(self):
        return f"Token<{self.type}:'{self.value}'>"

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    "BEGIN":Token(BEGIN, "BEGIN"),
    "DIV":Token(INTEGER_DIV, "DIV"),
    "END":Token(END, "END"),
    "INTEGER":Token(INTEGER, "INTEGER"),
    "PROGRAM":Token(PROGRAM, "PROGRAM"),
    "REAL":Token(REAL, "REAL"),
    "VAR":Token(VAR, "VAR"),
    "PROCEDURE":Token(PROCEDURE, PROCEDURE)
}

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################


class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.current_char = self.code[0]

    def advance(self):
        self.pos += 1
        if self.pos < len(code):
            self.current_char = self.code[self.pos]
        else:
            self.current_char = None

    def id(self):
        # [a-zA-Z][1-9a-zA-Z]*
        result = ''  

        while(self.current_char != None and self.current_char.isalnum()):
            result += self.current_char
            self.advance()    

        result = result.upper()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.current_char != None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == "{":
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            elif self.current_char.isalpha():
                return self.id()

            elif self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            elif self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            elif self.current_char == "/":
                self.advance()
                return Token(FLOAT_DIV, "/")

            elif self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            elif self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            elif self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            elif self.current_char == ",":
                self.advance()
                return Token(COMMA, ",")

            elif self.current_char == ".":
                self.advance()
                return Token(DOT, ".")

            elif self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")

            elif self.current_char == ":":
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    return Token(EQUALS, ":=")
                else:
                    return Token(COLON, ":")

            raise Exception("No matching tokens found")

        return Token(EOF, EOF)

    def number(self):
        number_string = self.code[self.pos]
        self.advance()

        while(self.current_char != None and self.current_char.isdigit()):
            number_string += self.current_char
            self.advance()    

        if self.current_char != ".":            
            return Token(INTEGER_CONST, int(number_string))
        else:
            number_string += "."
            self.advance()
            while(self.current_char != None and self.current_char.isdigit()):
                number_string += self.current_char
                self.advance()
            return Token(REAL_CONST, float(number_string))

    def peek(self):
        if self.pos+1 < len(code):
            return self.code[self.pos+1]
        else:
            self.current_char = None

    def skip_comment(self):
        while self.current_char != "}":
            self.advance()
        self.advance()

    def skip_whitespace(self):
        while self.current_char != None and self.current_char.isspace():
            self.advance()

###############################################################################
#                                                                             #
#  PARSER OBJECTS                                                             #
#                                                                             #
###############################################################################

class AssignNode:
    def __init__(self, name, value):
        self.name_node = name
        self.value_node = value

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class BlockNode:
    def __init__(self, declarations, compound_statements):
        self.declarations = declarations
        self.compound_statements = compound_statements

class CompoundNode:
    def __init__(self, statement_list):
        self.statement_list = statement_list

class IntegerNode:
    def __init__(self, token):
        self.token = token
        self.type = token.value

class IntegerConstNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp:
    pass

class ProcedureNode:
    def __init__(self, name, code):
        self.name = name
        self.code = code

class ProgramNode:
    def __init__(self, name, block):
        self.name = name
        self.block = block

class UnaryNode:
    def __init__(self, op, value):
        self.op = op
        self.value = value

class RealNode:
    def __init__(self, token):
        self.token = token
        self.type = token.value

class RealConstNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value

class VarDeclNode:
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class VarNode:
    def __init__(self, token):
        self.token = token
        self.name = token.value


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

'''
GRAMMERS:

program: PROGRAM variable SEMI block DOT
block: declarations compound_statement
declarations: VAR (declaration SEMI)+ | (PROCEDURE ID SEMI block SEMI)* empty
declaration: variable (COMMA variable) COLON type_spec SEMI
compound_statement: BEGIN statement_list END
statement_list: statement | statement SEMI statement_list
statement: compound_statement | assign_statement | empty
empty: 
assign_statement: variable EQUALS expr
expr: term ((PLUS | MINUS) term)*
term: factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*  
factor: INTEGER_CONST | REAL_CONST | LPAREN expr RPAREN
variable: ID
type_spec: INTEGER | REAL
'''

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = lexer.get_next_token()
        else:
            raise Exception(f"Parsing error, expected: {type}, got: {self.current_token.type}")

    def parse(self):
        return self.program()           

    def program(self):
        #program: PROGRAM variable SEMI block DOT
        self.eat(PROGRAM)
        var_name = self.current_token.value
        self.eat(ID)
        self.eat(SEMI)
        node = self.block()
        self.eat(DOT)
        return ProgramNode(var_name, node)

    def block(self):
        #block: declarations compound_statement
        decl_node = self.declarations()       
        cs_node = self.compound_statement()
        return BlockNode(decl_node, cs_node)    

    def declarations(self):
        #declarations: VAR (declaration SEMI)+ | (PROCEDURE ID SEMI block SEMI)* | empty
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                declarations.extend(self.declaration())
                self.eat(SEMI)
        
        if self.current_token.type == PROCEDURE:
            self.eat(PROCEDURE)
            procedure_name = self.current_token.value
            self.eat(ID)
            self.eat(SEMI)
            procedure_code = self.block()
            declarations.append(ProcedureNode(procedure_name, procedure_code))
            self.eat(SEMI)

        return declarations       

    def declaration(self):
        #declaration: variable (COMMA variable) COLON type
        variables = [self.variable()]
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            variables.append(self.variable())
    
        self.eat(COLON)
        type_node = self.type_spec()

        var_declarations = []
        for var_node in variables:
            var_declarations.append(VarDeclNode(var_node, type_node))

        return var_declarations

    def type_spec(self):
        #type_spec: INTEGER | REAL
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return IntegerNode(token)
        elif token.type == REAL:
            self.eat(REAL)
            return RealNode(token)

    def compound_statement(self):
        #compound_statement: BEGIN statement_list END
        self.eat(BEGIN)
        statements = self.statement_list()
        self.eat(END)
        return CompoundNode(statements)    

    def statement_list(self):
        #statement_list: statement | statement SEMI statement_list
        statement_list = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            statement_list.append(self.statement())
        return statement_list      

    def statement(self):
        #statement: compound_statement | assign_statement | empty
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assign_statement()
        else:
            node = self.empty()
        return node       

    def empty(self):
        #empty: 
        return NoOp()    

    def assign_statement(self):
        #assign_statement: variable EQUALS expr
        var_name = self.variable()
        self.eat(EQUALS)
        value = self.expr()

        node = AssignNode(var_name, value)
        return node             

    def expr(self):
        #expr: term ((PLUS | MINUS) term)*
        node = self.term()
        while self.current_token.type in [PLUS, MINUS]:
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)
            right = self.term()
            node = BinOpNode(node, op, right)        
        return node

    def term(self):
        #term: factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*         
        node = self.factor()
        while self.current_token.type in [MUL, INTEGER_DIV, FLOAT_DIV]:
            op = self.current_token
            if op.type == MUL:
                self.eat(MUL)
            elif op.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif op.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)
            right = self.factor()
            node = BinOpNode(node, op, right)
        return node

    def factor(self):
        #factor: unary (INTEGER_CONST | REAL_CONST | variable) | LPAREN expr RPAREN
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryNode(PLUS, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)   
            node = UnaryNode(MINUS, self.factor())                 
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            node = IntegerConstNode(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            node = RealConstNode(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
        elif token.type == ID:
            node = self.variable()
        else:
            raise Exception("No matching factor found")

        return node

    def variable(self):
        #variable: ID
        node = VarNode(self.current_token)
        self.eat(ID)
        return node
           

###############################################################################
#                                                                             #
#  visit PATTERN                                                            #
#                                                                             #
###############################################################################


class Visitor:
    def visit(self, node):
        function_name = "visit_" + type(node).__name__
        #print(f"Visiting: {function_name}")
        visit = getattr(self, function_name, self.no_valid_node)
        return visit(node)

    def no_valid_node(self):
        raise Exception("No valid node found to visit")


###############################################################################
#                                                                             #
#  SYMBOLS and SYBOLE TABLE                                                   #
#                                                                             #
###############################################################################


class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name = self.__class__.__name__,
            name = self.name
        )

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f"<{self.name}:{self.type}>"

    def __repr__(self):
        return "<{class_name}(name='{name}' type='{type}')>".format(
            class_name = self.__class__.__name__,
            name = self.name,
            type = self.type
        )

class SymbolTable:
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltInTypeSymbol("INTEGER"))
        self.define(BuiltInTypeSymbol("REAL"))

    def __str__(self):
        symbols = [symbol for symbol in self._symbols.values()]
        content = f"Symbols: {symbols}"
        return content

    def __repr__(self):
        return self.__str__()

    def define(self, symbol):
        print(f"Define: {symbol}")
        self._symbols[symbol.name] = symbol
    
    def lookup(self, symbol):
        print(f"Lookup: {symbol}")
        return self._symbols.get(symbol)


###############################################################################
#                                                                             #
#  SYMBOL TABLE VISITOR                                                       #
#                                                                             #
###############################################################################


class SemanticAnalyzer(Visitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_AssignNode(self, node):
        var_name = node.name_node.name
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:
            raise NameError(var_name)

        self.visit(node.value_node)

    def visit_BlockNode(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statements)

    def visit_BinOpNode(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_CompoundNode(self, node):
        for child in node.statement_list:
            self.visit(child)

    def visit_IntegerNode(self, node):
        return node.type

    def visit_IntegerConstNode(self, node):
        return node.value

    def visit_NoOp(self, node):
        pass

    def visit_ProcedureNode(self, node):
        pass

    def visit_ProgramNode(self, node):
        self.visit(node.block)

    def visit_RealNode(self, node):
        return node.type

    def visit_RealConstNode(self, node):
        return node.value

    def visit_UnaryNode(self, node):
        if node.op == MINUS:
            return -self.visit(node.value)
        elif node.op == PLUS: 
            return self.visit(node.value)

    def visit_VarDeclNode(self, node):
        var_name = node.var_node.name
        var_type = node.type_node.type
        symbol_type = self.symbol_table.lookup(var_type)
        var_symbol = (VarSymbol(var_name, symbol_type))

        if self.symbol_table.lookup(var_name) is not None:
            raise Exception(f"Duplicate symbol entry for '{var_name}'")

        self.symbol_table.define(var_symbol)

    def visit_VarNode(self, node):
        var_name = node.name
        var_symbol = self.symbol_table.lookup(var_name)

        if var_symbol is None:
            raise Exception(f"Symbol (identifier) not found: '{var_name}'")            


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################


class Interpreter(Visitor):
    def __init__(self, tree):
        self.tree = tree
        self.global_memory = {}
    
    def interpret(self):
        return self.visit(self.tree)

    def visit_AssignNode(self, node):
        var_name = node.name_node.name
        var_val = self.visit(node.value_node)
        self.global_memory[var_name] = var_val 

    def visit_BlockNode(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statements)

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == PLUS:
            return left + right
        elif node.op.type == MINUS:
            return left - right
        elif node.op.type == MUL:
            return left * right
        elif node.op.type == INTEGER_DIV:
            return left // right
        elif node.op.type == FLOAT_DIV:
            return left / right

    def visit_CompoundNode(self, node):
        for child in node.statement_list:
            self.visit(child)

    def visit_IntegerConstNode(self, node):
        return node.value

    def visit_NoOp(self, node):
        pass

    def visit_ProcedureNode(self, node):
        pass

    def visit_ProgramNode(self, node):
        self.visit(node.block)

    def visit_RealConstNode(self, node):
        return node.value

    def visit_UnaryNode(self, node):
        if node.op == MINUS:
            return -self.visit(node.value)
        elif node.op == PLUS: 
            return self.visit(node.value)

    def visit_VarDeclNode(self, node):
        pass

    def visit_VarNode(self, node):
        var_name = node.name
        var_value = self.global_memory.get(var_name)
        return var_value

###############################################################################
#                                                                             #
#  MAIN                                                                       #
#                                                                             #
###############################################################################

if __name__ == "__main__":
    code = """
program SymTab5;
    var 
    x : integer;
    y : real;

begin
    x := 2;
end.

    """
    print(f"Input: {code}")

    lexer = Lexer(code)
    parser = Parser(lexer)
    tree_head = parser.parse()
    print("Parsing complete")

    sem_analyzer = SemanticAnalyzer()
    sem_analyzer.visit_ProgramNode(tree_head)
    print(sem_analyzer.symbol_table)

    interpreter = Interpreter(tree_head)
    interpreter.interpret()
    result = interpreter.global_memory

    print(result)

