from lexer.token_types import TokenType, types, operators, creators


class Token:
    def __init__(self, token_type, value='', line=0, column=0):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{TokenType(self.token_type).name}: '{self.value}'. position({self.line}, {self.column})"

    @property
    def position(self):
        return f"({self.line}, {self.column})"

    @property
    def is_var_type(self):
        return self.token_type in types

    @property
    def is_operator(self):
        return self.token_type in operators

    def is_identifier(self):
        return self.token_type == TokenType.identifier

    @property
    def is_creator(self):
        return self.token_type in creators
