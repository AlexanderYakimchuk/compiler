import re

from lexer.token import Token
from lexer.token_types import TokenType, reserved_identifiers, arithmetic, \
    assigments, comparisons, parenthesis, braces, squares


class Lexer:
    def __init__(self, input_string):
        self.input = input_string
        self.position = 0
        self.line = 0
        self.column = 0

    def get_all_tokens(self):
        tokens = []
        token = self.get_next_token()
        while token.token_type != TokenType.eoi:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)
        return tokens

    def get_next_token(self):
        if self.position >= len(self.input):
            return Token(TokenType.eoi)
        self.skip_whitespaces_and_ends()
        if self.position >= len(self.input):
            return Token(TokenType.eoi)

        character = self.input[self.position]

        if character.isalpha() or character == '_':
            return self.recognize_identifier()

        if character.isdigit():
            return self.recognize_number()

        if self.is_arithmetic(character):
            return self.recognize_arithmetic_operator()

        if self.is_comparison(character):
            t = self.recognize_comparison_operator()
            if t:
                return t

        if character == ';':
            return self.recognize_semicolon()

        if character == ',':
            return self.recognize_coma()

        if character == '=':
            return self.recognize_assignment()

        if self.is_parenthesis(character):
            return self.recognize_parenthesis()

        if self.is_brace(character):
            return self.recognize_brace()

        if self.is_square(character):
            return self.recognize_square()

        if character == '"':
            return self.recognize_string()

        if character == '.':
            return self.recognize_reference()

        raise Exception(
            f'Unknown token at line {self.line} column {self.column}')

    def is_arithmetic(self, ch):
        return ch in arithmetic

    def is_comparison(self, ch):
        return ch in ['=', '<', '>']

    def is_parenthesis(self, ch):
        return ch in parenthesis

    def is_brace(self, ch):
        return ch in braces

    def is_square(self, ch):
        return ch in squares

    def skip_whitespaces_and_ends(self):
        character = self.input[self.position]
        while character == ' ' or character == '\n':
            self.position += 1
            self.column += 1
            if character == '\n':
                self.column = 0
                self.line += 1
            if self.position >= len(self.input):
                return
            character = self.input[self.position]

    def recognize_identifier(self):
        r = re.match(r'[a-zA-Z_]+[a-zA-Z0-9_]*', self.input[self.position:])
        self.position += r.end()
        self.column += r.end()
        identifier = r.group()
        token_type = TokenType.identifier
        if identifier in reserved_identifiers:
            token_type = reserved_identifiers[identifier]
        return Token(token_type, identifier, self.line, self.column - r.end())

    def recognize_number(self):
        r = re.match(r'[0-9]+(\.[0-9]+)?', self.input[self.position:])
        self.position += r.end()
        self.column += r.end()
        numb = r.group()
        token_type = TokenType.int_number
        if '.' in numb:
            token_type = TokenType.real_number
        return Token(token_type, numb, self.line, self.column - r.end())

    def recognize_arithmetic_operator(self):
        r = re.match(r'[+\-*/]=?', self.input[self.position:])
        self.position += r.end()
        self.column += r.end()
        op = r.group()
        token_type = arithmetic.get(op) or assigments.get(op)

        return Token(token_type, op, self.line, self.column - r.end())

    def recognize_comparison_operator(self):
        r = re.match(r'(==)|([<>]=?)', self.input[self.position:])
        if not r:
            return
        self.position += r.end()
        self.column += r.end()
        op = r.group()
        token_type = comparisons[op]

        return Token(token_type, op, self.line, self.column - r.end())

    def recognize_semicolon(self):
        self.position += 1
        self.column += 1
        return Token(TokenType.semicolon, ';', self.line, self.column - 1)

    def recognize_coma(self):
        self.position += 1
        self.column += 1
        return Token(TokenType.coma, ',', self.line, self.column - 1)

    def recognize_assignment(self):
        self.position += 1
        self.column += 1
        return Token(TokenType.assign, '=', self.line, self.column - 1)

    def recognize_parenthesis(self):
        p = self.input[self.position]
        self.position += 1
        self.column += 1
        return Token(parenthesis[p], p, self.line, self.column - 1)

    def recognize_brace(self):
        p = self.input[self.position]
        self.position += 1
        self.column += 1
        return Token(braces[p], p, self.line, self.column - 1)

    def recognize_square(self):
        p = self.input[self.position]
        self.position += 1
        self.column += 1
        return Token(squares[p], p, self.line, self.column - 1)

    def recognize_string(self):
        r = re.match(r'"[^"]*"', self.input[self.position:])
        self.position += r.end()
        self.column += r.end()
        string = r.group()
        return Token(TokenType.string_value, string, self.line, self.column - r.end())
    
    def recognize_reference(self):
        p = self.input[self.position]
        self.position += 1
        self.column += 1
        return Token(TokenType.reference, p, self.line, self.column - 1)

