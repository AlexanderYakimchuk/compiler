from lexer.lexer import Lexer


from my_parser.my_parser import Parser
from simulator.simulator import Simulator

with open('examples/built_in_types.txt', 'r') as file:
    code = file.read()

lexer = Lexer(code)
tokens = lexer.get_all_tokens()
tokens = tokens
parser = Parser(tokens)
simulator = Simulator(parser)
simulator.simulate()
