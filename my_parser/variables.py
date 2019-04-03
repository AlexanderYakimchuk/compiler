from lexer.token_types import TokenType
from my_parser.expressions import Value


class Variable:
    def __init__(self, type_, name, value):
        self.type_ = type_
        self.name = name
        self.value = value


class Event:
    def __init__(self, name, quantity, ticket_types=None):
        self.name = name
        self.quantity = quantity
        self.ticket_types = ticket_types
        self.__calculated = False

    @property
    def type_(self):
        return str(type(self)).split('.')[-1][:-2]

    def value(self, mem):
        if not self.__calculated:
            return self.get_value(mem)
        return Value(self.type_, self)

    def get_value(self, mem):
        self.name = self.name.get_value(mem)
        if self.name.type_ != TokenType.string_value:
            raise Exception("Event name must be string")
        self.name = self.name.value
        self.quantity = self.quantity.get_value(mem)
        if self.quantity.type_ != TokenType.int_number:
            raise Exception("Event quantity must be int")
        self.quantity = self.quantity.value
        if self.ticket_types:
            self.ticket_types = self.ticket_types.get_value(mem).value
        self.__calculated = True
        return Value(self.type_, self)

    def __add__(self, other):
        if isinstance(other, int):
            self.quantity += other
        elif isinstance(other, TicketType):
            self.ticket_types.append(other)
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            self.quantity -= other
        elif isinstance(other, TicketType):
            self.sub_ticket_type(other)
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            self.quantity *= other
        return self

    def sub_ticket_type(self, ticket_type):
        if ticket_type.attendees:
            raise Exception("Can not delete ticket type with attendees.")
        self.ticket_types.remove(ticket_type)


class TicketType:
    def __init__(self, name, price, quantity, attendees=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.attendees = attendees

    @property
    def type_(self):
        return str(type(self)).split('.')[-1][:-2]

    @property
    def value(self):
        return self

    def __add__(self, other):
        if isinstance(other, int):
            self.quantity += other
        elif isinstance(other, Attendee):
            self.attendees.append(other)
        return self


class Attendee:
    def __init__(self, name, place):
        self.name = name
        self.place = place

    @property
    def type_(self):
        return str(type(self)).split('.')[-1][:-2]

    @property
    def value(self):
        return self
