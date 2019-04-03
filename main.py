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
    ticketType t = TicketType(name="VIP", quantity=5 * 2, price=99.99 - 1);
    ticketType t1 = TicketType(name="Standart", quantity=t.quantity * 2, price=49.99);
    int a = 2;
    a = a + 3;
    t.quantity = t.quantity + 1.0;
    print(t.quantity);
    print(t1.quantity);
    print(a);'''
lexer = Lexer(code1)
tokens = lexer.get_all_tokens()
tokens = tokens
parser = Parser(tokens)
simulator = Simulator(parser)
# parser.parse()
simulator.simulate()
# exp.display()

# code = '''True and (5 > 4)'''
# lexer = Lexer(code)
# tokens = lexer.get_all_tokens()
# parser = Parser(tokens)
# exp = parser.parse_expression()

# print(value)