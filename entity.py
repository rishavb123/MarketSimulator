class Entity:

    def __init__(self, initial_capital=0):
        self.holdings = {
            "capital": initial_capital
        }

    def get_holding(self, name):
        return self.holdings.get(name, 0)
    
    def get_capital(self):
        return self.get_holding("capital")
    
    def tick(self):
        pass