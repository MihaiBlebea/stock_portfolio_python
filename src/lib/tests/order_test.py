from src.lib import Stock, Currency
from src.lib import Order, Direction


aapl = Stock("AAPL", 0.56, 10.02, Currency.USD)


def test_can_init_buy_order():
    buy_order = Order.buy(aapl, 22.22, Currency.GBP, 10)

    assert buy_order.stock == aapl, f"Expected: AAPL, got {buy_order.stock.symbol}"
    assert (
        buy_order.currency == Currency.GBP
    ), f"Expected: Currency.GBP, got {buy_order.currency}"
    assert (
        buy_order.direction == Direction.BUY
    ), f"Expected: Direction.BUY, got {buy_order.stock.direction}"
    assert buy_order.is_buy() == True, f"Expected: True, got {buy_order.is_buy()}"
    assert buy_order.is_sell() == False, f"Expected: False, got {buy_order.is_sell()}"
    assert buy_order.price == 22.22, f"Expected: 22.22, got {buy_order.price}"
    assert buy_order.get_price_in_currency() != 22.22, f"Expected: not 22.22, got 22.22"
    assert buy_order.quantity == 10, f"Expected: 10, got {buy_order.quantity}"


if __name__ == "__main__":
    test_can_init_buy_order()
