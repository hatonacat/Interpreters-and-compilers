from errors import LexerError
from tokens import build_reserved_keywords, Token, TokenType, RESERVED_KEYWORDS


###############################################################################
#                                                                             #
#  LEXER                                                                      #
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

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.current_char = self.code[0]
        # Token line and column number
        self.line_no = 1
        self.column_no = 1

    def advance(self):
        if self.current_char == "\n":
            self.line_no += 1
            self.column_no = 0

        self.pos += 1
        if self.pos < len(self.code):
            self.current_char = self.code[self.pos]
            self.column_no += 1
        else:
            self.current_char = None

    def error(self):
        s = "Lexer error on '{lexeme}' line: {line_no} column: {column_no}".format(
            lexeme = self.current_char,
            line_no = self.line_no,
            column_no = self.column_no,
        )
        raise LexerError(message=s)

    def id(self):
        # [a-zA-Z][1-9a-zA-Z]*
        token = Token(None, None, self.line_no, self.column_no)
        
        result = ''  
        while(self.current_char != None and self.current_char.isalnum()):
            result += self.current_char
            self.advance()    

        token_type = RESERVED_KEYWORDS.get(result.upper())
        if token_type == None:
            token.type = TokenType.ID
            token.value = result
        else:
            token.type = token_type
            token.value = result.upper()

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

            if self.current_char.isalpha():
                return self.id()

            if self.current_char == ":" and self.peek() == "=":
                token = Token(
                    type=TokenType.ASSIGN,
                    value=TokenType.ASSIGN.value,
                    line_no=self.line_no,
                    column_no=self.column_no,
                )
                self.advance()
                self.advance()
                return token

            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                self.error()
            else:
                token = Token(
                    type = token_type,
                    value = self.current_char,
                    line_no = self.line_no,
                    column_no = self.column_no,
                )
                self.advance()
                return token

            raise Exception("No matching tokens found")

        return Token(EOF, EOF)

    def number(self):
        number_string = self.code[self.pos]
        self.advance()

        while(self.current_char != None and self.current_char.isdigit()):
            number_string += self.current_char
            self.advance()    

        if self.current_char != ".":            
            return Token(TokenType.INTEGER_CONST, int(number_string))
        else:
            number_string += "."
            self.advance()
            while(self.current_char != None and self.current_char.isdigit()):
                number_string += self.current_char
                self.advance()
            return Token(TokenType.REAL_CONST, float(number_string))

    def peek(self):
        if self.pos+1 < len(self.code):
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