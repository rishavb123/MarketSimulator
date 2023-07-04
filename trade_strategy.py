from entity import Entity

class TradeStrategy(Entity):

    def __init__(self, name, trade_func, initial_capital=0):
        super().__init__(name, initial_capital)
        self.trade_func = trade_func

    def tick(self):
        super().tick()
        self.trade_func(self)