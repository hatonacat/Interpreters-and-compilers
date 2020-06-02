from errors import ErrorCode, SemanticError
from symbols import (ProcedureSymbol, VarSymbol, ScopedSymbolTable)

_SHOULD_LOG_SCOPE = True

###############################################################################
#                                                                             #
#  VISIT PATTERN                                                              #
#                                                                             #
###############################################################################


class Visitor:
    def visit(self, node):
        function_name = "visit_" + type(node).__name__
        visit = getattr(self, function_name, self.no_valid_node)
        print(f"Visiting: {function_name}")
        return visit(node)

    def no_valid_node(self):
        raise Exception("No valid node found to visit")


###############################################################################
#                                                                             #
#  SYMBOL TABLE VISITOR                                                       #
#                                                                             #
###############################################################################


class SemanticAnalyzer(Visitor):
    def __init__(self):
        self.scope = ScopedSymbolTable(scope_name='Global', scope_level=1)
        self.current_scope = None

    def error(self, error_code, token):
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}'
        )

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(msg)

    def visit_AssignNode(self, node):
        var_name = node.name_node.name
        var_symbol = self.current_scope.lookup(var_name)
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

    def visit_ProcedureDeclNode(self, node):
        proc_name = node.name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.insert(proc_symbol)

        self.log(f"ENTER scope: {proc_name}")
        procedure_scope = ScopedSymbolTable(
            scope_name = proc_name,
            scope_level = self.current_scope.scope_level + 1,
            enclosing_scope = self.current_scope
        )
        self.current_scope = procedure_scope

        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.type)
            param_name = param.var_node.name
            var_symbol = VarSymbol(param_name, param_type)

            if self.current_scope.lookup(param_name, current_scope_only=True):
                self.error(
                    error_code=ErrorCode.DUPLICATE_ID,
                    token = param.var_node.token,
                )

            self.current_scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)

        self.visit(node.block)

        self.log(procedure_scope)
        self.current_scope = self.current_scope.enclosing_scope
        self.log(f"LEAVE scope: {proc_name}")


    def visit_ProgramNode(self, node):
        self.log("ENTER scope: global")
        global_scope = ScopedSymbolTable(
            scope_name = 'Global',
            scope_level = 1,
            enclosing_scope = self.current_scope, #None
        )
        self.current_scope = global_scope

        self.visit(node.block)
        self.log(global_scope)
        self.enclosing_scope = self.current_scope.enclosing_scope
        self.log("LEAVE scope: global")

    def visit_RealNode(self, node):
        return node.type

    def visit_RealConstNode(self, node):
        return node.value

    def visit_UnaryNode(self, node):
        if node.op == "MINUS":
            return -self.visit(node.value)
        elif node.op == "PLUS": 
            return self.visit(node.value)

    def visit_VarDeclNode(self, node):
        var_name = node.var_node.name
        var_type = node.type_node.type
        symbol_type = self.current_scope.lookup(var_type)
        var_symbol = (VarSymbol(var_name, symbol_type))

        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(
                error_code=ErrorCode.DUPLICATE_ID,
                token = node.var_node.token,
            )

        self.current_scope.insert(var_symbol)

    def visit_VarNode(self, node):
        var_name = node.name
        var_symbol = self.current_scope.lookup(var_name)

        if var_symbol is None:
            raise self.error(error_code=ErrorCode.ID_NOT_FOUND, token=node.token)            


###############################################################################
#                                                                             #
#  SOURCE TO SOURCE COMPILER VISITOR                                          #
#                                                                             #
###############################################################################


class SourceToSourceCompiler(Visitor):
    def __init__(self):
        self.scope = ScopedSymbolTable(scope_name='Main', scope_level=0)
        self.current_scope = None
        self.s = []
        self.code = ""

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(msg)

    def visit_AssignNode(self, node):
        var_name = node.name_node.name
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise NameError(var_name)

        left = self.visit(node.name_node)
        right = self.visit(node.value_node)

        self.s.append(f"{self.indent()}{left} := {right}")

    def visit_BlockNode(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statements)

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        return f"{left} {node.op.value} {right}"

    def visit_CompoundNode(self, node):
        self.s.append(f"\n{self.indent(-1)}begin")
        for child in node.statement_list:
            self.visit(child)
        self.s.append(f"{self.indent(-1)}end")

    def visit_IntegerNode(self, node):
        return node.type

    def visit_IntegerConstNode(self, node):
        return node.value

    def visit_NoOp(self, node):
        pass

    def visit_ProcedureDeclNode(self, node):
        proc_name = node.name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.insert(proc_symbol)

        proc_string = f"{self.indent()}procedure {proc_name}"

        self.log(f"ENTER scope: {proc_name}")
        procedure_scope = ScopedSymbolTable(
            scope_name = proc_name,
            scope_level = self.current_scope.scope_level + 1,
            enclosing_scope = self.current_scope
        )
        self.current_scope = procedure_scope

        param_list = []
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.type)
            param_name = param.var_node.name
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)
            param_list.append(f"{param_name}{self.level()} : {param_type}")

        parameters_string = " ".join(param_list)
        self.s.append(
             f"{proc_string}({parameters_string});"
        )

        self.visit(node.block)
        self.s[-1] += "; {{END OF {name}}}".format(name=proc_name)

        self.current_scope = self.current_scope.enclosing_scope
        self.log(f"LEAVE scope: {proc_name}")


    def visit_ProgramNode(self, node):
        self.log("ENTER scope: global")
        self.s.append(f"Program {node.name}{self.level()};")
        global_scope = ScopedSymbolTable(
            scope_name = 'Global',
            scope_level = 1,
            enclosing_scope = self.current_scope, #None
        )
        self.current_scope = global_scope

        self.visit(node.block)
        self.enclosing_scope = self.current_scope.enclosing_scope
        self.s[-1] += ". {{END OF {name}}}".format(name=node.name)
        self.code = "\n".join(self.s)
        self.log("LEAVE scope: global")

    def visit_RealNode(self, node):
        return node.type

    def visit_RealConstNode(self, node):
        return node.value

    def visit_UnaryNode(self, node):
        if node.op == "MINUS":
            return -self.visit(node.value)
        elif node.op == "PLUS": 
            return self.visit(node.value)

    def visit_VarDeclNode(self, node):
        var_name = node.var_node.name
        var_type = node.type_node.type
        symbol_type = self.current_scope.lookup(var_type)
        var_symbol = (VarSymbol(var_name, symbol_type))

        self.s.append(
            f"{self.indent()}var {var_name}{self.level()} : {var_type};"
        )

        if self.current_scope.lookup(var_name, current_scope_only=True) is not None:
            raise Exception(f"Duplicate symbol entry for '{var_name}'")

        self.current_scope.insert(var_symbol)

    def visit_VarNode(self, node):
        var_name = node.name
        var_symbol = self.current_scope.lookup(var_name)

        if var_symbol is None:
            raise Exception(f"Symbol (identifier) not found: '{var_name}'")

        var_level = var_symbol.scope.scope_level

        return "<{var_name}{scope}:{symbol}>".format(
            var_name = var_name,
            scope = var_level,
            symbol = var_symbol.type
        )


    def indent(self, adjuster=0):
        '''
        Helper printer function, returns required tab number for given level
        '''
        return (self.current_scope.scope_level + adjuster) * "    "

    def level(self):
        '''
        Helper function, returns current level
        '''
        if self.current_scope == None:
            return 0
        return self.current_scope.scope_level