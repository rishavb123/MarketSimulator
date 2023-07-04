class OrderBook:

    def __init__(self, symbol) -> None:
        self.buy_orders = {}
        self.sell_orders = {}
        self.symbol = symbol

    def at(self, price, sender, quantity=1):
        self.sell_orders[sender] = [price, quantity]

    def bid(self, price, sender, quantity=1):
        self.buy_orders[sender] = [price, quantity]

    def withdraw_at(self, sender):
        del self.sell_orders[sender]

    def withdraw_bid(self, sender):
        del self.buy_orders[sender]

    def match_orders(self):
        matched_trades = []

        def get_highest_bid():
            return min(self.buy_orders.keys(), key=lambda sender: self.buy_orders[sender][0])
    
        def get_lowest_at():
            return max(self.sell_orders.keys(), key=lambda sender: self.sell_orders[sender][0])

        def make_trade(buy_sender, sell_sender, price, quantity):
            matched_trades.append((buy_sender, sell_sender, price, quantity))
            self.buy_orders[buy_sender][1] -= quantity
            if self.buy_orders[buy_sender][1] == 0:
                del self.buy_orders[buy_sender]

            self.sell_orders[sell_sender][1] -= quantity
            if self.sell_orders[sell_sender][1] == 0:
                del self.sell_orders[sell_sender]

            buy_sender.update_holdings(self.symbol, quantity)
            sell_sender.update_holdings(self.symbol, -quantity)

            buy_sender.add_capital(-price * quantity)
            sell_sender.add_capital(price * quantity)

        if len(self.buy_orders.keys()) > 0 and len(self.sell_orders.keys()) > 0:
            highest_bid_sender = get_highest_bid()
            lowest_at_sender = get_lowest_at()

            while self.buy_orders[highest_bid_sender][0] >= self.sell_orders[lowest_at_sender][0]:
                price = self.sell_orders[lowest_at_sender][0]
                quantity = min(
                    self.buy_orders[highest_bid_sender][1], 
                    self.sell_orders[lowest_at_sender][1], 
                    lowest_at_sender.get_holding(self.symbol),
                    int(highest_bid_sender.get_capital() / price)
                )
                make_trade(highest_bid_sender, lowest_at_sender, price, quantity)

                if len(self.buy_orders.keys()) == 0 or len(self.sell_orders.keys()) == 0:
                    break

                highest_bid_sender = get_highest_bid()
                lowest_at_sender = get_lowest_at()

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