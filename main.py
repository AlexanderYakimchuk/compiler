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
                print(p);
            }
            t = true and (p > 4);'''
code1 = '''
    int p = 1;
    while p < 5 {
        p = p + 1;
    }'''
lexer = Lexer(code)
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