from src.lib import Stock, Currency, Order, Position, Portfolio
from src.weight import Weight
from src.smart_portfolio import SmartPortfolio
from pprint import pprint

if __name__ == "__main__":
    aapl = Stock("AAPL", 0.56, 10.02, Currency.USD)
    tsla = Stock("TSLA", 0, 165.08, Currency.USD)

    # print(aapl.get_price_in_currency(Currency.GBP))

    # print(aapl == aapl)

    order_aapl_buy_one = Order.buy(aapl, 11.50, Currency.GBP, 10)
    order_aapl_buy_two = Order.buy(aapl, 12.50, Currency.GBP, 20)
    order_aapl_sell = Order.sell(aapl, 10.50, Currency.GBP, 12)
    order_tsla_one = Order.buy(tsla, 180.50, Currency.GBP, 5)

    p_aapl = Position(
        aapl,
        [order_aapl_buy_one, order_aapl_buy_two, order_aapl_sell],
    )

    p_tsla = Position(
        tsla,
        [order_tsla_one],
    )
    portfolio = SmartPortfolio([p_aapl, p_tsla])

    # print(portfolio)

    # print(portfolio.get_total_value())

    # pprint(portfolio.get_position("tsla"))
    portfolio.add_order(Order.sell(tsla, 190.0, Currency.GBP, 4))

    pprint(portfolio.get_position("aapl"))

    # pprint(portfolio.get_weight())

    pprint(portfolio.get_weight().values)

    w = Weight({"AAPL": 0.6, "TSLA": 0.4})

    print(portfolio.recalibrate(w, False))

    # pprint(portfolio.get_position("AAPL"))

    googl = Stock("GOOGL", 0, 16.16, Currency.USD)
    portfolio.add_calibrated_position(googl, 0.3)

    pprint(portfolio.get_weight().data)
