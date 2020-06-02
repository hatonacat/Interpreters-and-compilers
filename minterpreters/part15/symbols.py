_SHOULD_LOG_SCOPE = False

###############################################################################
#                                                                             #
#  SYMBOLS and SYMBOL TABLE                                                   #
#                                                                             #
###############################################################################


class Symbol:
    def __init__(self, name, type=None, scope=None):
        self.name = name
        self.type = type
        self.scope = scope

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

class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None):
        super().__init__(name)
        self.params = params if params is not None else []

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.params,
        )

    def __repr__(self):
        return self.__str__()

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

class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self._init_builtins()

    def _init_builtins(self):
        self.insert(BuiltInTypeSymbol("INTEGER"))
        self.insert(BuiltInTypeSymbol("REAL"))

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope', self.enclosing_scope.scope_name if self.enclosing_scope else None)
        ):
            lines.append('{:15}: {}'.format(header_name, header_value))
        h2 = '\nScope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('{0:>7}: {1!r}'.format(key, value))
            for key, value in self._symbols.items()
        )
        s = '\n'.join(lines) + '\n'
        return s

    def __repr__(self):
        return self.__str__()

    def insert(self, symbol):
        self.log(f"insert: {symbol}, Scope name: {self.scope_name}")
        self._symbols[symbol.name] = symbol
        symbol.scope = self

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(msg)

    def lookup(self, name, current_scope_only=False):
        symbol = self._symbols.get(name)
        self.log(f"Lookup: {symbol}, Scope name: {self.scope_name}")

        if symbol is not None:
            return symbol
            
        if current_scope_only:
            return None

        self.log(f"Symbol {symbol} not in current scope")
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)