from util import UniversalTicker, print_header

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
        print_header(self.name, 100)

        total = 0

        print(f"symbol\t\tquantity\t\tcurrent price\t\tvalue")
        
        for symbol in self.holdings:
            price = UniversalTicker.get_instance().shared_data["companies"].get(symbol, None)
            if price is None:
                price = 1
            else:
                price = price.price_per_share()
            quantity = self.get_holding(symbol)
            total += price * quantity
            print(f"{symbol}\t\t{quantity:0.8f}\t\t{price:0.8f}\t\t{price * quantity:0.8f}")

        print(f"total\t\t{total:0.8f}\t\t{1:0.8f}\t\t{total:0.8f}")