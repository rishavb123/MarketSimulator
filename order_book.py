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
                    trade_quantity = min(buy_quantity, sell_quantity)
                    matched_trades.append((buy_sender, sell_sender, trade_quantity, sell_price))
                    buy_quantity -= trade_quantity
                    sell_quantity -= trade_quantity

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