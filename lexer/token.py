from lexer.token_types import TokenType, types, operators, creators, \
    ref_operators, unary_operators


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

    @property
    def is_identifier(self):
        return self.token_type == TokenType.identifier

    @property
    def is_reference(self):
        return self.token_type == TokenType.reference

    @property
    def is_creator(self):
        return self.token_type in creators

    @property
    def is_ref_operator(self):
        return self.token_type in ref_operators

    @property
    def is_unary_operator(self):
        return self.token_type in unary_operators

