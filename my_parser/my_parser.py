from lexer.token import Token
from lexer.token_types import TokenType, operators, ref_operators
from my_parser.comands import Declaration, IfStatement, Assigment, \
    WhileStatement, PrintStatement
from my_parser.expressions import Expression, Block
from my_parser.variables import Event, TicketType, Attendee, Array


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cur_index = 0
        self.commands = []
        self.variables = {}
        self.__last_arr_type = None

    @property
    def cur_token(self):
        return self.tokens[self.cur_index]

    def parse(self):
        while self.cur_token.token_type != TokenType.eoi:
            self.commands.append(self.parse_command())

    def parse_command(self):
        if self.cur_token.is_var_type:
            return self.parse_declaration()
        elif self.cur_token.token_type == TokenType.if_st:
            return self.parse_if()
        elif self.cur_token.token_type == TokenType.identifier:
            return self.parse_assigment()
        elif self.cur_token.token_type == TokenType.while_st:
            return self.parse_while()
        elif self.cur_token.token_type == TokenType.print_st:
            return self.parse_print()

    def get_max_priority(self, tokens):
        max_prior = -float('inf')
        max_index = 0
        open_p_numb = 0
        open_s_numb = 0
        ignore_op = False
        for i in range(len(tokens)):
            if tokens[i].is_creator:
                ignore_op = True
            if (not ignore_op) and tokens[i].is_operator:
                op_prior = operators[tokens[i].token_type] - open_p_numb * 100 - open_s_numb * 1000
                if op_prior >= max_prior:
                    max_prior = op_prior
                    max_index = i
            elif tokens[i].token_type == TokenType.l_parenthesis:
                open_p_numb += 1
            elif tokens[i].token_type == TokenType.r_parenthesis:
                open_p_numb -= 1
                if open_p_numb == 0 and ignore_op:
                    ignore_op = False
            if tokens[i].token_type == TokenType.l_square:
                open_s_numb += 1
            if tokens[i].token_type == TokenType.r_square:
                open_s_numb -= 1
            if open_p_numb < 0:
                raise Exception("Invalid parenthesis")
            if open_s_numb < 0:
                raise Exception("Invalid squares")
        if open_p_numb != 0:
            raise Exception("Invalid parenthesis")
        if open_s_numb != 0:
            raise Exception("Invalid squares")
        return max_index

    def trim_edges(self, tokens):
        while tokens[0].token_type == TokenType.l_parenthesis and tokens[-1].token_type == TokenType.r_parenthesis:
            tokens1 = tokens[1:-1]
            p_numb = 0
            for t in tokens1:
                if t.token_type == TokenType.l_parenthesis:
                    p_numb += 1
                elif t.token_type == TokenType.r_parenthesis:
                    p_numb -= 1
                if p_numb < 0:
                    return tokens
            tokens = tokens1
        return tokens

    def parse_expression(self, tokens=None):
        if not tokens:
            end = self.skip(TokenType.semicolon)
            tokens = self.tokens[self.cur_index:end]
        tokens = self.trim_edges(tokens)
        index = self.get_max_priority(tokens)
        if tokens[index].is_creator:
            return self.parse_creator(tokens)
        left = None
        right = None
        if tokens[index].is_operator:
            if not tokens[index + 1:]:
                raise Exception(f'Invalid operator {tokens[index]}')
            if not tokens[:index]:
                if tokens[index].is_unary_operator:
                    tokens = [Token(TokenType.int_number, '0')] + tokens
                    index += 1
                else:
                    raise Exception(f'Invalid operator {tokens[index]}')

            left = self.parse_expression(tokens[:index])
            if tokens[index].token_type == TokenType.l_square:
                if tokens[-1].token_type != TokenType.r_square:
                    raise Exception(f'Expected ] at {tokens[-1].position}')
                right = self.parse_expression(tokens[index + 1:-1])
            else:
                right = self.parse_expression(tokens[index + 1:])
        return Expression(token_type=tokens[index],
                          left=left,
                          right=right,
                          tokens=tokens)

    def skip(self, token_type):
        i = self.cur_index
        while self.tokens[i].token_type != token_type and self.tokens[i].token_type != TokenType.eoi:
            i += 1
        return i

    def skip_local(self, index, tokens, token_types):
        if not isinstance(token_types, list):
            token_types = [token_types]
        i = index
        while i < len(tokens) and tokens[i].token_type not in token_types:
            i += 1
        return i

    def parse_declaration(self):
        type_ = self.tokens[self.cur_index]
        self.cur_index += 1
        el_type = None
        if type_.token_type == TokenType.arr:
            el_type = self.tokens[self.cur_index].token_type
            self.__last_arr_type = el_type
            self.cur_index += 1
        if self.cur_token.is_identifier:
            name = self.cur_token
        else:
            raise Exception(f'Expected identifier in ({self.cur_token.line}, {self.cur_token.column})')
        self.cur_index += 1
        value = None
        if self.cur_token.token_type == TokenType.assign:
            self.cur_index += 1
            value = self.parse_expression()
        end = self.skip(TokenType.semicolon)
        self.cur_index = end + 1
        self.variables[name] = value
        return Declaration(type_.token_type, name.value, value, el_type)

    def parse_if(self):
        self.cur_index += 1
        end = self.skip(TokenType.l_brace)
        cond = self.parse_expression(self.tokens[self.cur_index:end])
        self.cur_index = end + 1
        if_block = self.parse_block()
        else_block = None
        if self.cur_token.token_type == TokenType.else_st:
            if self.tokens[self.cur_index + 1].token_type == TokenType.l_brace:
                self.cur_index += 2
                else_block = self.parse_block()
            else:
                raise Exception('Expected left brace after else statement.')
        return IfStatement(cond, if_block, else_block)

    def parse_block(self):
        end = self.skip(TokenType.r_brace)
        if self.tokens[end].token_type == TokenType.eoi:
            raise Exception(f'Expected right brace {self.tokens[end].line}')
        block = Block()
        while self.cur_token.token_type != TokenType.r_brace:
            block.commands.append(self.parse_command())
        self.cur_index += 1
        return block

    def parse_creator(self, tokens):
        if tokens[0].token_type == TokenType.array_creator:
            return self.parse_array_creator(tokens)
        index = 1
        params = {}
        self.expect(tokens[index], TokenType.l_parenthesis)
        index += 1
        while tokens[index].token_type != TokenType.r_parenthesis:
            self.expect(tokens[index], TokenType.identifier)
            name = tokens[index]
            index += 1
            self.expect(tokens[index], TokenType.assign)
            index += 1
            end = self.skip_local(index, tokens, [TokenType.coma,
                                                  TokenType.r_parenthesis])
            value = self.parse_expression(tokens[index:end])
            index = end
            params[name.value] = value
            if tokens[index].token_type == TokenType.r_parenthesis:
                break
            index += 1
        if tokens[0].token_type == TokenType.event_creator:
            return Event(**params)
        if tokens[0].token_type == TokenType.ticket_type_creator:
            return TicketType(**params)
        if tokens[0].token_type == TokenType.attendee_creator:
            return Attendee(**params)

    def parse_array_creator(self, tokens):
        index = 1
        values = []
        self.expect(tokens[index], TokenType.l_parenthesis)
        index += 1
        while tokens[index].token_type != TokenType.r_parenthesis:
            end = self.skip_local(index, tokens, [TokenType.coma,
                                                  TokenType.r_parenthesis])
            value = self.parse_expression(tokens[index:end])
            index = end
            values.append(value)
            if tokens[index].token_type == TokenType.r_parenthesis:
                break
            index += 1
        return Array(self.__last_arr_type, values)

    def parse_assigment(self):
        end = self.skip(TokenType.assign)
        name = self.parse_ref_expression(self.tokens[self.cur_index:end])
        self.cur_index = end
        if self.cur_token.token_type != TokenType.assign:
            raise Exception(f'Expected assigment at {self.cur_token.position}')
        self.cur_index += 1
        end = self.skip(TokenType.semicolon)
        value = self.parse_expression(self.tokens[self.cur_index:end])
        self.cur_index = end + 1
        return Assigment(name, value)

    def get_max_priority_for_ref(self, tokens):
        max_prior = -float('inf')
        max_index = 0
        for i in range(len(tokens)):
            if tokens[i].is_ref_operator:
                op_prior = ref_operators[tokens[i].token_type]
                if op_prior >= max_prior:
                    max_prior = op_prior
                    max_index = i

        return max_index

    def parse_ref_expression(self, tokens):
        index = self.get_max_priority_for_ref(tokens)
        left = None
        right = None
        if tokens[index].is_operator:
            if not (tokens[:index] and tokens[index + 1:]):
                raise Exception(f'Invalid operator {tokens[index]}')

            left = self.parse_expression(tokens[:index])
            if tokens[index].token_type == TokenType.l_square:
                if tokens[-1].token_type != TokenType.r_square:
                    raise Exception(f'Expected ] at {tokens[-1].position}')
                right = self.parse_expression(tokens[index + 1:-1])
            else:
                right = self.parse_expression(tokens[index + 1:])
        return Expression(token_type=tokens[index],
                          left=left,
                          right=right,
                          tokens=tokens)

    def parse_while(self):
        self.cur_index += 1
        end = self.skip(TokenType.l_brace)
        cond = self.parse_expression(self.tokens[self.cur_index:end])
        self.cur_index = end + 1
        block = self.parse_block()
        return WhileStatement(cond, block)

    def parse_print(self):
        self.cur_index += 1
        if self.cur_token.token_type != TokenType.l_parenthesis:
            raise Exception(f'Expected ( at {self.cur_token.position}')
        self.cur_index += 1
        end = self.skip(TokenType.semicolon)
        if self.tokens[end - 1].token_type != TokenType.r_parenthesis:
            raise Exception(f'Expected ) at {self.tokens[end - 1].position}')
        value = self.parse_expression(self.tokens[self.cur_index:end - 1])
        self.cur_index = end + 1
        return PrintStatement(value)

    def expect(self, token, token_type):
        if token.token_type != token_type:
            raise Exception("Unexpected token.")
