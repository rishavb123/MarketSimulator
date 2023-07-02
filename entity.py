class Entity:

    def __init__(self, initial_capital=0):
        self.holdings = {
            "capital": initial_capital
        }

    def get_holding(self, name):
        return self.holdings.get(name, 0)
    
    def update_holdings(self, name, number):
        self.holdings[name] = self.get_holding(name) + number

    def get_capital(self):
        return self.get_holding("capital")
    
    def add_capital(self, number):
        self.update_holdings("capital", number)

    def tick(self):
        pass