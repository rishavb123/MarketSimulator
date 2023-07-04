class Entity:

    def __init__(self, name, initial_capital=0):
        self.name = name
        self.holdings = {
            "capital": initial_capital
        }

    def get_holding(self, symbol):
        return self.holdings.get(symbol, 0)
    
    def update_holdings(self, symbol, number):
        self.holdings[symbol] = self.get_holding(symbol) + number

    def get_capital(self):
        return self.get_holding("capital")
    
    def add_capital(self, number):
        self.update_holdings("capital", number)

    def tick(self):
        pass

    def display_holdings(self):
        line_length = 100
        print("-" * line_length)
        print(" " * ((line_length - (self.name)) // 2) + self.name)
        print("-" * line_length)
        for symbol in self.holdings:
            print(f"{symbol}\t\t{self.get_holding(symbol)}")