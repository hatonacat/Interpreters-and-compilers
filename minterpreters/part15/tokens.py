from enum import Enum

###############################################################################
#                                                                             #
#  Token                                                                      #
#                                                                             #
###############################################################################

class Token:
    def __init__(self, type, value, line_no=None, column_no=None):
        self.type = type
        self.value = value
        self.line_no = line_no
        self.column_no = column_no
        #print(self)

    def __str__(self):
        return "Token({type}, value={value}, position={line_no}:{column_no})".format(
            type = self.type,
            value = repr(self.value),
            line_no = self.line_no,
            column_no = self.column_no,
        )

    def __repr__(self):
        return self.__str__()

class TokenType(Enum):
    # single-character token types
    PLUS          = '+'
    MINUS         = '-'
    MUL           = '*'
    FLOAT_DIV     = '/'
    LPAREN        = '('
    RPAREN        = ')'
    SEMI          = ';'
    DOT           = '.'
    COLON         = ':'
    COMMA         = ','
    # block of reserved words
    PROGRAM       = 'PROGRAM'  # marks the beginning of the block
    INTEGER       = 'INTEGER'
    REAL          = 'REAL'
    INTEGER_DIV   = 'DIV'
    VAR           = 'VAR'
    PROCEDURE     = 'PROCEDURE'
    BEGIN         = 'BEGIN'
    END           = 'END'      # marks the end of the block
    # misc
    ID            = 'ID'
    INTEGER_CONST = 'INTEGER_CONST'
    REAL_CONST    = 'REAL_CONST'
    ASSIGN        = ':='
    EOF           = 'EOF'

def build_reserved_keywords():
    '''
    Converts token types between PROGRAM and END
    into a reserved keyword dictionary
    '''
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.PROGRAM)
    end_index = tt_list.index(TokenType.END)
    reserved_keywords = {
        token_type.value:token_type for 
        token_type in tt_list[start_index:end_index+1]
    }
    return reserved_keywords

RESERVED_KEYWORDS = build_reserved_keywords()

if __name__ == "__main__":
    #build_reserved_keywords()
    print(RESERVED_KEYWORDS)












