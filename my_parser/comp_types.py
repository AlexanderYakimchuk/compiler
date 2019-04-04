from copy import deepcopy

from lexer.token_types import TokenType

comp_types = {
    (TokenType.int_number, TokenType.int_number): {
        TokenType.plus: (TokenType.int_number, lambda a, b: a + b),
        TokenType.minus: (TokenType.int_number, lambda a, b: a - b),
        TokenType.times: (TokenType.int_number, lambda a, b: a * b),
        TokenType.div: (TokenType.real_number, lambda a, b: a / b),
        TokenType.eq: (TokenType.bool_value, lambda a, b: a == b),
        TokenType.gt: (TokenType.bool_value, lambda a, b: a > b),
        TokenType.gte: (TokenType.bool_value, lambda a, b: a >= b),
        TokenType.lt: (TokenType.bool_value, lambda a, b: a < b),
        TokenType.lte: (TokenType.bool_value, lambda a, b: a <= b),
    },
    (TokenType.int_number, TokenType.real_number): {
        TokenType.plus: (TokenType.real_number, lambda a, b: a + b),
        TokenType.minus: (TokenType.real_number, lambda a, b: a - b),
        TokenType.times: (TokenType.real_number, lambda a, b: a * b),
        TokenType.div: (TokenType.real_number, lambda a, b: a / b),
        TokenType.eq: (TokenType.bool_value, lambda a, b: a == b),
        TokenType.gt: (TokenType.bool_value, lambda a, b: a > b),
        TokenType.gte: (TokenType.bool_value, lambda a, b: a >= b),
        TokenType.lt: (TokenType.bool_value, lambda a, b: a < b),
        TokenType.lte: (TokenType.bool_value, lambda a, b: a <= b),
    },
    (TokenType.real_number, TokenType.int_number): {
        TokenType.plus: (TokenType.real_number, lambda a, b: a + b),
        TokenType.minus: (TokenType.real_number, lambda a, b: a - b),
        TokenType.times: (TokenType.real_number, lambda a, b: a * b),
        TokenType.div: (TokenType.real_number, lambda a, b: a / b),
        TokenType.eq: (TokenType.bool_value, lambda a, b: a == b),
        TokenType.gt: (TokenType.bool_value, lambda a, b: a > b),
        TokenType.gte: (TokenType.bool_value, lambda a, b: a >= b),
        TokenType.lt: (TokenType.bool_value, lambda a, b: a < b),
        TokenType.lte: (TokenType.bool_value, lambda a, b: a <= b),
    },
    (TokenType.real_number, TokenType.real_number): {
        TokenType.plus: (TokenType.real_number, lambda a, b: a + b),
        TokenType.minus: (TokenType.real_number, lambda a, b: a - b),
        TokenType.times: (TokenType.real_number, lambda a, b: a * b),
        TokenType.div: (TokenType.real_number, lambda a, b: a / b),
        TokenType.eq: (TokenType.bool_value, lambda a, b: a == b),
        TokenType.gt: (TokenType.bool_value, lambda a, b: a > b),
        TokenType.gte: (TokenType.bool_value, lambda a, b: a >= b),
        TokenType.lt: (TokenType.bool_value, lambda a, b: a < b),
        TokenType.lte: (TokenType.bool_value, lambda a, b: a <= b),
    },
    (TokenType.bool_value, TokenType.bool_value): {
        TokenType.eq: (TokenType.bool_value, lambda a, b: a == b),
        TokenType.and_st: (TokenType.bool_value, lambda a, b: (a and b)),
        TokenType.or_st: (TokenType.bool_value, lambda a, b: (a or b)),
    },
    ('Event', TokenType.int_number): {
        TokenType.plus: ('Event', lambda a, b: deepcopy(a) + b),
        TokenType.minus: ('Event', lambda a, b: deepcopy(a) - b),
        TokenType.times: ('Event', lambda a, b: deepcopy(a) * b),
    },
    ('Event', 'TicketType'): {
        TokenType.plus: ('Event', lambda a, b: deepcopy(a) + b),
        TokenType.minus: ('Event', lambda a, b: deepcopy(a) - b),
    },
    ('TicketType', TokenType.int_number): {
        TokenType.plus: ('TicketType', lambda a, b: deepcopy(a) + b),
        TokenType.minus: ('TicketType', lambda a, b: deepcopy(a) - b),
        TokenType.times: ('TicketType', lambda a, b: deepcopy(a) * b),
    },
    ('TicketType', 'Attendee'): {
        TokenType.plus: ('TicketType', lambda a, b: deepcopy(a) + b),
    },
    ('TicketTypeArr', TokenType.int_number): {
        TokenType.l_square: ('TicketType', lambda a, b: a[b]),
    },
    ('AttendeeArr', TokenType.int_number): {
        TokenType.l_square: ('Attendee', lambda a, b: a[b]),
    },
    ('intArray', TokenType.int_number): {
        TokenType.l_square: (TokenType.int_number, lambda a, b: a[b]),
    },
    ('realArray', TokenType.int_number): {
        TokenType.l_square: (TokenType.real_number, lambda a, b: a[b]),
    },
    ('booleanArray', TokenType.int_number): {
        TokenType.l_square: (TokenType.bool_value, lambda a, b: a[b]),
    },
    ('stringArray', TokenType.int_number): {
        TokenType.l_square: (TokenType.string_value, lambda a, b: a[b]),
    },
}

eq_types = [
    (TokenType.event, 'Event'),
    ('Event', 'Event'),
    (TokenType.ticket_type, 'TicketType'),
    ('TicketType', 'TicketType'),
    (TokenType.attendee, 'Attendee'),
    ('Attendee', 'Attendee'),
    (TokenType.real, TokenType.real_number),
    (TokenType.real_number, TokenType.real_number),
    (TokenType.real, TokenType.int_number),
    (TokenType.real_number, TokenType.int_number),
    (TokenType.int, TokenType.int_number),
    (TokenType.int_number, TokenType.int_number),
    (TokenType.boolean, TokenType.bool_value),
    (TokenType.bool_value, TokenType.bool_value),
    (TokenType.string, TokenType.string_value),
    (TokenType.string_value, TokenType.string_value),
    ('intArray', TokenType.array_creator),
    ('intArray', 'intArray'),
    ('realArray', TokenType.array_creator),
    ('realArray', 'realArray'),
    ('booleanArray', TokenType.array_creator),
    ('booleanArray', 'booleanArray'),
    ('stringArray', TokenType.array_creator),
    ('stringArray', 'stringArray'),
]

type_transfers = {
    TokenType.event: 'Event',
    TokenType.ticket_type: 'TicketType',
    TokenType.attendee: 'Attendee',
    TokenType.real: TokenType.real_number,
    TokenType.int: TokenType.int_number,
    TokenType.boolean: TokenType.bool_value,
    TokenType.string: TokenType.string_value,
    'intArray': 'intArray',
    'realArray': 'realArray',
    'booleanArray': 'booleanArray',
    'stringArray': 'stringArray'
}
