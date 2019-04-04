from lexer.token_types import TokenType
from my_parser.comp_types import comp_types, type_transfers


def fit_value(type_):
    types = {
        TokenType.int_number: int,
        TokenType.real_number: float,
        TokenType.string_value: str,
        TokenType.bool_value: lambda a: True if a == 'true' or a is True else False
    }
    if types.get(type_):
        return types[type_]


class Value:
    key = 0

    def __init__(self, type_, value):
        Value.key += 1
        self.key = Value.key
        self.type_ = type_
        fit = fit_value(type_)
        self.value = value
        if fit:
            self.value = fit_value(type_)(self.value)

    def __repr__(self):
        return f"{self.type_}: {self.value}"

    def make_operation(self, op, other):
        type1 = type_transfers.get(self.type_) or self.type_
        type2 = type_transfers.get(other.type_) or other.type_
        allowed_op = comp_types.get((type1, type2))
        if not allowed_op:
            raise Exception(f'Incompatible types {type1} and {type2}.')
        type_, func = allowed_op.get(op)
        if not func:
            raise Exception(f"Unresolved operation {op} for {type1} and {type2}.")
        res = func(self.value, other.value)
        if isinstance(res, Value):
            return res
        return Value(type_, func(self.value, other.value))


class Expression:
    def __init__(self, token_type, left, right, tokens=None):
        self.token = token_type
        self.left = left
        self.right = right
        self.tokens = tokens
        self.value_ = None

    def __repr__(self):
        return f"{self.token}; left={self.left}; right={self.right}"

    @property
    def is_identifier(self):
        return len(self.tokens) == 1 and self.token.is_identifier

    def value(self, mem):
        return self.get_value(mem)

    def get_value(self, mem):
        if not self.token.is_operator:
            if self.token.token_type == TokenType.identifier:
                value = mem.get(self.token.value)
                if not value:
                    raise Exception(f"Variable {self.token.value} is not declared.")
                return value
            return Value(self.token.token_type, self.token.value)

        left = self.left.value(mem)

        if self.token.is_reference:
            if not isinstance(self.right, Expression) or not self.right.is_identifier:
                raise Exception(f'Expected identifier at {self.token.position}')
            if not hasattr(left.value, self.right.token.value):
                raise Exception(f'Object of type {left.type_} has not attr {self.right.token.value}')
            attr = getattr(left.value, self.right.token.value)
            return attr
        right = self.right.value(mem)
        return left.make_operation(self.token.token_type, right)

    def display(self):
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.token
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.token
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line,
                    second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.token
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line,
                    second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.token
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (
                m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (
                m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in
                                             zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class Block:
    def __init__(self):
        self.commands = []
