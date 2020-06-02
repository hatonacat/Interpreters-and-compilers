from errors import Error, ErrorCode, ParserError
from parser_objects import (AssignNode, BinOpNode, BlockNode, CompoundNode, IntegerConstNode, 
                            IntegerNode, NoOp, ParamNode, ProcedureDeclNode, ProgramNode, 
                            RealConstNode, RealNode, UnaryNode, VarDeclNode, VarNode)
from tokens import Token, TokenType, RESERVED_KEYWORDS

_SHOULD_LOG_SCOPE = True

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

'''
GRAMMERS:

program: PROGRAM variable SEMI block DOT
block: declarations compound_statement
declarations :  
    (VAR (declaration SEMI)+)*
    | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
    | empty
declaration: variable (COMMA variable) COLON type_spec SEMI
formal_parameter_list: 
    formal_parameters
    | formal_parameters SEMI formal_parameter_list
formal_parameters : ID (COMMA ID)* COLON type_spec
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
        self.log(f'Next token: {self.current_token}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
            self.log(f'Next token: {self.current_token}')
        else:
            self.error(
                error_code = ErrorCode.UNEXPECTED_TOKEN,
                token = self.current_token,
                expected = token_type,
            )

    def error(self, error_code, token, expected=None):
        message = f'{error_code.value} -> {token}'
        if expected: message += f' Expected -> {expected}'
        raise ParserError(
            error_code = error_code,
            token = token,
            message = message
        )

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(msg)

    def parse(self):
        return self.program()           

    def program(self):
        #program: PROGRAM variable SEMI block DOT
        self.eat(TokenType.PROGRAM)
        var_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.SEMI)
        node = self.block()
        self.eat(TokenType.DOT)
        self.log("Parsing complete")
        return ProgramNode(var_name, node)

    def block(self):
        #block: declarations compound_statement
        decl_node = self.declarations()       
        cs_node = self.compound_statement()
        return BlockNode(decl_node, cs_node)    

    def declarations(self):
        '''
        declarations :  
            (VAR (variable_declaration SEMI)+)* procedure_declaration*
            | empty
        '''
        declarations = []
        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                declarations.extend(self.declaration())
                self.eat(TokenType.SEMI)
        
        while self.current_token.type == TokenType.PROCEDURE:
            proc_decl = self.procedure_declaration()
            declarations.append(proc_decl)
        
        return declarations       

    def declaration(self):
        #declaration: variable (COMMA variable) COLON type
        variables = [self.variable()]
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            variables.append(self.variable())
    
        self.eat(TokenType.COLON)
        type_node = self.type_spec()

        var_declarations = []
        for var_node in variables:
            var_declarations.append(VarDeclNode(var_node, type_node))

        return var_declarations

    def procedure_declaration(self):
        '''
        PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI
        '''
        self.eat(TokenType.PROCEDURE)
        name = self.current_token.value
        self.eat(TokenType.ID)
        parameter_list = None

        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            parameter_list = self.formal_parameter_list()
            self.eat(TokenType.RPAREN)
        
        self.eat(TokenType.SEMI)
        block = self.block()
        self.eat(TokenType.SEMI)    

        return ProcedureDeclNode(name, parameter_list, block)

    def formal_parameter_list(self):
        '''
        formal_parameter_list: 
            formal_parameters
            | formal_parameters SEMI formal_parameter_list
        '''
        formal_parameters = self.formal_parameters()
        if self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            formal_parameters.extend(self.formal_parameter_list())

        return formal_parameters

    def formal_parameters(self):
        '''
        formal_parameters : ID (COMMA ID)* COLON type_spec
        '''
        variables = [VarNode(self.current_token)]
        self.eat(TokenType.ID)
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            variables.append(VarNode(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()

        param_list = []
        for var_node in variables:
            param_list.append(ParamNode(var_node, type_node))

        return param_list

    def type_spec(self):
        #type_spec: INTEGER | REAL
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return IntegerNode(token)
        elif token.type == TokenType.REAL:
            self.eat(TokenType.REAL)
            return RealNode(token)

    def compound_statement(self):
        #compound_statement: BEGIN statement_list END
        self.eat(TokenType.BEGIN)
        statements = self.statement_list()
        self.eat(TokenType.END)
        return CompoundNode(statements)    

    def statement_list(self):
        #statement_list: statement | statement SEMI statement_list
        statement_list = [self.statement()]
        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            statement_list.append(self.statement())
        return statement_list      

    def statement(self):
        #statement: compound_statement | assign_statement | empty
        if self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.ID:
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
        self.eat(TokenType.ASSIGN)
        value = self.expr()

        node = AssignNode(var_name, value)
        return node             

    def expr(self):
        #expr: term ((PLUS | MINUS) term)*
        node = self.term()
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token
            if op.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif op.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            right = self.term()
            node = BinOpNode(node, op, right)        
        return node

    def term(self):
        #term: factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*         
        node = self.factor()
        while self.current_token.type in [TokenType.MUL, TokenType.INTEGER_DIV, TokenType.FLOAT_DIV]:
            op = self.current_token
            if op.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif op.type == TokenType.INTEGER_DIV:
                self.eat(TokenType.INTEGER_DIV)
            elif op.type == TokenType.FLOAT_DIV:
                self.eat(TokenType.FLOAT_DIV)
            right = self.factor()
            node = BinOpNode(node, op, right)
        return node

    def factor(self):
        #factor: unary (INTEGER_CONST | REAL_CONST | variable) | LPAREN expr RPAREN
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryNode(TokenType.PLUS, self.factor())
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)   
            node = UnaryNode(TokenType.MINUS, self.factor())                 
        elif token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            node = IntegerConstNode(token)
        elif token.type == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            node = RealConstNode(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
        elif token.type == TokenType.ID:
            node = self.variable()
        else:
            self.error(
                error_code = ErrorCode.UNEXPECTED_TOKEN,
                token = token
            )

        return node

    def variable(self):
        #variable: ID
        node = VarNode(self.current_token)
        self.eat(TokenType.ID)
        return node
