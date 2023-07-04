from company import Company
from trade_strategy import TradeStrategy
from order_book import OrderBook
from util import create_price_generator, UniversalTicker, print_header

def run_experiment(objs, num_ticks=24 * 30 * 6, wait_for_input=False, exclude_names=[], print_rate=100):
    exclude_names = set(exclude_names)
    objs = [UniversalTicker.get_instance(), *objs]

    for i in range(num_ticks):
        for o in objs:
            o.tick()

        if i % print_rate == 0:
            print_header(f"Tick {i}:", 150)

            for o in objs:
                if hasattr(o, "display_holdings") and o.name not in exclude_names:
                    o.display_holdings()

            if wait_for_input: input()

    print_header(f"Tick {i}:", 150)

    for o in objs:
        if hasattr(o, "display_holdings") and o.name not in exclude_names:
            o.display_holdings()


def experiment_1():
    company = Company("AAA", noise_generator=create_price_generator(100, 1, 1))
    company.release_shares(1000)
    order_book = OrderBook(company.symbol)

    def trade_func(trader):
        bought_price = UniversalTicker.get_instance().shared_data.get("bought_price", None)
        if trader.get_capital() > company.price_per_share() * 50 and bought_price is None:
            order_book.bid(company.price_per_share(), trader, 50)
            order_book.at(company.price_per_share(), company, 50)
            bought_price = company.price_per_share()
        if bought_price is not None and company.price_per_share() > bought_price * 1.1:
            order_book.bid(company.price_per_share(), company, 1)
            order_book.at(company.price_per_share(), trader, 1)
            if trader.get_holding(company.symbol) == 0:
                bought_price = None
        UniversalTicker.get_instance().shared_data["bought_price"] = bought_price

    trader = TradeStrategy("trader", trade_func, initial_capital=10)
    
    run_experiment([company, trader, order_book], wait_for_input=False, exclude_names=[company.symbol])

def main():
    experiment_1()

if __name__ == "__main__":
    main()