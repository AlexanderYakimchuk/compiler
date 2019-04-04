from lexer.token_types import TokenType
from my_parser.comp_types import eq_types, type_transfers
from my_parser.expressions import Value
from my_parser.variables import Array


class Command:
    def execute(self, mem):
        raise NotImplementedError


class Declaration(Command):
    def __init__(self, type_, name, value, el_type):
        self.type_ = type_
        self.name = name
        self.value = value
        self.el_type = el_type

    def execute(self, mem):
        type_ = self.type_
        if self.type_ == TokenType.arr:
            type_ = Array(self.el_type).type_
        if not self.value:
            mem[self.name] = Value(type_, None)
            return

        value = self.value.get_value(mem)
        if (type_, value.type_) not in eq_types:
            raise Exception(f'Incompatible type for var {self.name} expected {type_}, received {value.type_}')
        value.type_ = type_transfers[type_]
        mem[self.name] = Value(value.type_, value.value)


class IfStatement(Command):
    def __init__(self, cond, if_block, else_block=None):
        self.cond = cond
        self.if_block = if_block
        self.else_block = else_block

    def execute(self, mem):
        cond = self.cond.get_value(mem)
        if cond.type_ != TokenType.bool_value:
            raise Exception(f'Expected {TokenType.bool_value.name} after "if".')
        block = self.if_block if cond.value is True else self.else_block
        if not block:
            return
        for command in block.commands:
            command.execute(mem)


class WhileStatement(Command):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def execute(self, mem):
        cond = self.cond.get_value(mem)
        if cond.type_ != TokenType.bool_value:
            raise Exception(f'Expected {TokenType.bool_value.name} after "if".')
        while cond.value:
            for command in self.block.commands:
                command.execute(mem)
            cond = self.cond.get_value(mem)


class Assigment(Command):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def execute(self, mem):
        old_value = self.name.get_value(mem)
        # if not old_value:
        #     raise Exception(f"Variable {name.value} is not declared.")
        value = self.value.get_value(mem=mem)
        if (old_value.type_, value.type_) not in eq_types:
            raise Exception(
                f'Incompatible type for var expected {old_value.type_}')
        if self.name.is_identifier:
            mem[self.name.token.value] = Value(old_value.type_, value.value)
            return

        old_value.value = value.value


class PrintStatement(Command):
    def __init__(self, value):
        self.value = value

    def execute(self, mem):
        value = self.value.get_value(mem=mem)
        print(value.value)
