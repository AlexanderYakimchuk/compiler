from lexer.token_types import TokenType
from my_parser.comp_types import eq_types, type_transfers
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
        self.quantity = self.quantity.get_value(mem)
        if self.quantity.type_ != TokenType.int_number:
            raise Exception("Event quantity must be int")
        if self.ticket_types:
            self.ticket_types = self.ticket_types.get_value(mem)
        else:
            self.ticket_types = Value('TicketTypeArr', [])
        self.__calculated = True
        return Value(self.type_, self)

    def __add__(self, other):
        if isinstance(other, int):
            self.quantity.value += other
        elif isinstance(other, TicketType):
            self.ticket_types.value.append(other)
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            self.quantity.value -= other
        elif isinstance(other, TicketType):
            self.sub_ticket_type(other)
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            self.quantity.value *= other
        return self

    def sub_ticket_type(self, ticket_type):
        if ticket_type.attendees.value:
            raise Exception("Can not delete ticket type with attendees.")
        self.ticket_types.value.remove(ticket_type)


class TicketType:
    def __init__(self, name, price, quantity, attendees=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.attendees = attendees
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
            raise Exception("TicketType name must be string")
        self.quantity = self.quantity.get_value(mem)
        if self.quantity.type_ != TokenType.int_number:
            raise Exception("TicketType quantity must be int")
        self.price = self.price.get_value(mem)
        if self.price.type_ != TokenType.real_number:
            raise Exception("TicketType price must be real")
        if self.attendees:
            self.attendees = self.attendees.get_value(mem)
        else:
            self.attendees = Value('AttendeeArr', [])
        self.__calculated = True
        return Value(self.type_, self)

    def __add__(self, other):
        if isinstance(other, int):
            self.quantity.value += other
        elif isinstance(other, Attendee):
            self.attendees.value.append(other)
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            if not self.attendees or self.quantity.value - other >= len(self.attendees.value):
                self.quantity.value -= other
            else:
                raise Exception(f'Min allowed quantity is {len(self.attendees.value)}')
        return self


class Attendee:
    def __init__(self, name, place):
        self.name = name
        self.place = place
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
            raise Exception("Attendee name must be string")
        self.place = self.place.get_value(mem)
        if self.place.type_ != TokenType.int_number:
            raise Exception("TicketType quantity must be int")
        self.__calculated = True
        return Value(self.type_, self)


class Array:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.__calculated = False

    @property
    def type_(self):
        return f'{self.type.value}Array'

    @property
    def len(self):
        return Value(TokenType.int_number, len(self.value))

    def value(self, mem):
        if not self.__calculated:
            return self.get_value(mem)
        return Value(self.type_, self)

    def get_value(self, mem):
        if self.value:
            for i in range(len(self.value)):
                value = self.value[i].get_value(mem)
                type_ = type_transfers.get(value.type_) or value.type_
                if (self.type, type_) not in eq_types:
                    raise Exception(f'Invalid element type. Expected {self.type} received {type_}')
                self.value[i] = Value(type_, value.value)
        self.__calculated = True
        return Value(self.type_, self)

    def __getitem__(self, item):
        return self.value[item]
