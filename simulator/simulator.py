class Simulator:
    def __init__(self, parser):
        self.parser = parser
        self.mem = {}

    def simulate(self):
        self.parser.parse()
        for command in self.parser.commands:
            command.execute(self.mem)
