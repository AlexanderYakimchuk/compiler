from lexer.lexer import Lexer


from my_parser.my_parser import Parser
from simulator.simulator import Simulator

code = '''  int i = 2;
            if 0 > 0 {
                i = 7;
            } else {
                if true {
                    int c = 0;
                }
                int t = 8;
                real p = ((4 + 4) * 5);
            }
            p = 9.0;
            event e = Event(name="my event", quantity=5) + 100 + 4;
            bool t = 9 + 4 == 9 + 2 + 2;
            while p < 15 {
                p = p + 1;
            }
            t = true and (p > 4);'''
code1 = '''
    arr string my_arr = Array("sdfs", "sdfsdfsd", "");
    int i = 0;
    while i < my_arr.len {
        print(my_arr[i]);
        i = i + 1;
    }
    print(my_arr);
    event e = Event(name="my ivent", quantity=4);
    ticketType t = TicketType(name="VIP", price=39.99, quantity=10);
    event e1;
    e1 = Event(name=e.name, quantity=4);
    e = e + t;
    int a = -2;
    print(-a);
    t = t + Attendee(name="I", place=5);
    e.ticket_types[0].name = "NEW";
    print(e.ticket_types[(30 - 30) * 2].name);'''

code2 = '''
        t[4].a[2+3]'''
lexer = Lexer(code1)
tokens = lexer.get_all_tokens()
tokens = tokens
parser = Parser(tokens)
simulator = Simulator(parser)
# parser.parse()
simulator.simulate()

# code = '''True and (5 > 4)'''
# lexer = Lexer(code2)
# tokens = lexer.get_all_tokens()
# parser = Parser(tokens)
# exp = parser.parse_expression()

# print(value)