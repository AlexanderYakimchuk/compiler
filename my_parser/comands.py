from lexer.token_types import TokenType
from my_parser.comp_types import eq_types, type_transfers
from my_parser.expressions import Value


class Command:
    def execute(self, mem):
        raise NotImplementedError


class Declaration(Command):
    def __init__(self, type_, name, value):
        self.type_ = type_
        self.name = name
        self.value = value

    def execute(self, mem):
        if not self.value:
            mem[self.name] = Value(self.type_, None)
            return

        value = self.value.get_value(mem)
        if (self.type_, value.type_) not in eq_types:
            raise Exception(f'Incompatible type for var {self.name} expected {self.type_}')
        value.type_ = type_transfers[self.type_]
        mem[self.name] = value


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
        old_value.value = value.value


class PrintStatement(Command):
    def __init__(self, value):
        self.value = value

    def execute(self, mem):
        value = self.value.get_value(mem=mem)
        print(value.value)
