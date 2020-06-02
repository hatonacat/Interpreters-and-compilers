from errors import SemanticError
from tokens import TokenType
from visitor import Visitor

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

        if node.op.type == TokenType.PLUS:
            return left + right
        elif node.op.type == TokenType.MINUS:
            return left - right
        elif node.op.type == TokenType.MUL:
            return left * right
        elif node.op.type == TokenType.INTEGER_DIV:
            return left // right
        elif node.op.type == TokenType.FLOAT_DIV:
            return left / right

    def visit_CompoundNode(self, node):
        for child in node.statement_list:
            self.visit(child)

    def visit_IntegerConstNode(self, node):
        return node.value

    def visit_NoOp(self, node):
        pass

    def visit_ProcedureDeclNode(self, node):
        pass

    def visit_ProgramNode(self, node):
        self.visit(node.block)

    def visit_RealConstNode(self, node):
        return node.value

    def visit_UnaryNode(self, node):
        if node.op == "MINUS":
            return -self.visit(node.value)
        elif node.op == "PLUS": 
            return self.visit(node.value)

    def visit_VarDeclNode(self, node):
        pass

    def visit_VarNode(self, node):
        var_name = node.name
        var_value = self.global_memory.get(var_name)
        return var_value