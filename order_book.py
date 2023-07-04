class OrderBook:

    def __init__(self, symbol) -> None:
        self.buy_orders = {}
        self.sell_orders = {}
        self.symbol = symbol

    def at(self, price, sender, quantity=1):
        self.sell_orders[sender] = price, quantity

    def bid(self, price, sender, quantity=1):
        self.buy_orders[sender] = price, quantity

    def match_orders(self):
        matched_trades = []

        for buy_sender, (buy_price, buy_quantity) in self.buy_orders.items():
            for sell_sender, (sell_price, sell_quantity) in self.sell_orders.items():
                if buy_price >= sell_price: 
                    trade_quantity = min(buy_quantity, sell_quantity, sell_sender.get_holdings(self.symbol))
                    matched_trades.append((buy_sender, sell_sender, trade_quantity, sell_price))
                    buy_quantity -= trade_quantity
                    sell_quantity -= trade_quantity
                    buy_sender.update_holdings(self.symbol, trade_quantity)
                    sell_sender.update_holdings(self.symbol, -trade_quantity)

                    if buy_quantity == 0:
                        del self.buy_orders[buy_sender]
                    else:
                        self.buy_orders[buy_sender] = buy_price, buy_quantity

                    if sell_quantity == 0:
                        del self.sell_orders[sell_sender]
                    else:
                        self.sell_orders[sell_sender] = sell_price, sell_quantity

                    if buy_quantity == 0:
                        break

        return matched_trades

    def tick(self):
        return self.match_orders()
            
class MultiSymbolOrderBook:

    def __init__(self) -> None:
        self.order_books = {}

    def get_order_book(self, symbol):
        if symbol not in self.order_books:
            self.order_books[symbol] = OrderBook(symbol)
        return self.order_books[symbol]
    
    def at(self, symbol, price, sender, quantity=1):
        self.get_order_book(symbol).at(price, sender, quantity)
    
    def bid(self, symbol, price, sender, quantity=1):
        self.get_order_book(symbol).bid(price, sender, quantity)

    def match_orders(self):
        matched_trades = {}
        for symbol, order_book in self.order_books.items():
            matched_trades[symbol] = order_book.match_orders()
        return matched_trades

    def tick(self):
        return self.match_orders()