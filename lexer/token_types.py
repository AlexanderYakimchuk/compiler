from enum import Enum


class TokenType(Enum):
    # identifiers and literals
    identifier = 'identifier'
    int = 'int'
    real = 'real'
    string = 'string'
    boolean = 'boolean'
    event = 'event'
    ticket_type = 'ticketType'
    attendee = 'attendee'
    event_creator = 'event creator'
    ticket_type_creator = 'ticket type creator'
    attendee_creator = 'attendee creator'
    if_st = 'if'
    else_st = 'else'
    for_st = 'for'
    while_st = 'while'
    struct_st = 'struct'
    and_st = 'and'
    or_st = 'or'
    not_st = 'not'
    bool_value = 'bool value'
    int_number = 'int number'
    real_number = 'real number'
    string_value = 'string value'
    print_st = 'print'
    arr = 'array'
    array_creator = 'array creator'

    # arithmetic operators
    plus = '+'
    minus = '-'
    times = '*'
    div = '/'

    # comparison operators
    eq = '=='
    gt = '>'
    lt = '<'
    gte = '>='
    lte = '<='

    # assigment
    assign = '='
    plus_assign = '+='
    minus_assign = '-='
    times_assign = '*='
    div_assign = '/='

    # parenthesis
    l_parenthesis = '('
    r_parenthesis = ')'

    #braces
    l_brace = '{'
    r_brace = '}'

    #squares
    l_square = '['
    r_square = ']'

    #ref
    reference = '.'

    semicolon = ';'
    coma = ','

    # eoi
    eoi = 'end of input'


reserved_identifiers = {
    'int': TokenType.int,
    'real': TokenType.real,
    'string': TokenType.string,
    'bool': TokenType.boolean,
    'if': TokenType.if_st,
    'else': TokenType.else_st,
    'while': TokenType.while_st,
    'and': TokenType.and_st,
    'or': TokenType.or_st,
    'not': TokenType.not_st,
    'true': TokenType.bool_value,
    'false': TokenType.bool_value,
    'event': TokenType.event,
    'ticketType': TokenType.ticket_type,
    'attendee': TokenType.attendee,
    'Event': TokenType.event_creator,
    'TicketType': TokenType.ticket_type_creator,
    'Attendee': TokenType.attendee_creator,
    'print': TokenType.print_st,
    'arr': TokenType.arr,
    'Array': TokenType.array_creator
}

arithmetic = {
    '+': TokenType.plus,
    '-': TokenType.minus,
    '*': TokenType.times,
    '/': TokenType.div,
}

assigments = {
    '+=': TokenType.plus_assign,
    '-=': TokenType.minus_assign,
    '*=': TokenType.times_assign,
    '/=': TokenType.div_assign.div_assign,
    '=': TokenType.assign
}

comparisons = {
    '==': TokenType.eq,
    '>': TokenType.gt,
    '>=': TokenType.gte,
    '<': TokenType.lt,
    '<=': TokenType.lte
}

parenthesis = {
    '(': TokenType.l_parenthesis,
    ')': TokenType.r_parenthesis
}

braces = {
    '{': TokenType.l_brace,
    '}': TokenType.r_brace
}

squares = {
    '[': TokenType.l_square,
    ']': TokenType.r_square
}

types = [TokenType.int, TokenType.string, TokenType.boolean, TokenType.real,
         TokenType.event, TokenType.ticket_type, TokenType.attendee, TokenType.arr]

operators = {
    TokenType.eq: 8,
    TokenType.gt: 8,
    TokenType.gte: 8,
    TokenType.lt: 8,
    TokenType.lte: 8,
    TokenType.or_st: 6,
    TokenType.and_st: 5,
    TokenType.plus: 3,
    TokenType.minus: 3,
    TokenType.times: 2,
    TokenType.div: 2,
    TokenType.reference: 1,
    TokenType.l_square: 1}

ref_operators = {
    TokenType.reference: 1,
    TokenType.l_square: 1
}

unary_operators = [
    TokenType.plus, TokenType.minus
]

creators = [TokenType.event_creator, TokenType.ticket_type_creator,
            TokenType.attendee_creator, TokenType.array_creator]
