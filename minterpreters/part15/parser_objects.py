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

class ParamNode:
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class ProcedureDeclNode:
    def __init__(self, name, params, block):
        self.name = name
        self.params = params
        self.block = block

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
