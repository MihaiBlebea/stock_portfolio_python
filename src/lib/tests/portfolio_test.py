from src.lib import Stock, Order, Portfolio, Currency, Position, Weight


def setup_portfolio():
    aapl = Stock("AAPL", 0.56, 10.02, Currency.USD)
    tsla = Stock("TSLA", 0, 22.02, Currency.USD)

    port = Portfolio(
        [
            Position(
                aapl,
                [
                    Order.buy(aapl, 22.2, Currency.GBP, 10),
                    Order.buy(aapl, 25.5, Currency.GBP, 20),
                    Order.sell(aapl, 23.3, Currency.GBP, 5),
                ],
            )
        ]
    )

    port.add_order(Order.buy(tsla, 25.55, Currency.GBP, 100))

    return port


def test_can_init_portfolio():
    port = setup_portfolio()

    assert port.currency == Currency.GBP, f"Expected: Currency.GBP, got {port.currency}"
    assert len(port.positions) == 2, f"Expected: 2, got {len(port.positions)}"
    assert (
        len(port.get_position("aapl").orders) == 3
    ), f"Expected: 3, got {len(port.get_position('aapl').orders)}"
    assert (
        port.get_position("AAPL").get_total_value() == 596.25
    ), f"Expected: 596.25, got {port.get_position('AAPL').get_total_value()}"
    assert (
        port.get_total_value() == 3151.25
    ), f"Expected: 3151.25, got {port.get_total_value()}"


def test_can_get_weights():
    port = setup_portfolio()

    w = port.get_weight()

    assert isinstance(w, Weight), f"Expected: True, got False"
    assert (
        w.get_key("AAPL") == 0.18921063070210234
    ), f"Expected: 0.18921063070210234, got {w.get_key('AAPL')}"
    assert (
        w.get_key("TSLA") == 0.8107893692978977
    ), f"Expected: 0.8107893692978977, got {w.get_key('TSLA')}"


def test_can_recalibrate_portfolio():
    port = setup_portfolio()

    orders = port.recalibrate(Weight({"AAPL": 0.5, "TSLA": 0.5}))

    w = port.get_weight()

    assert w.get_key("AAPL") == 0.5, f"Expected: 0.5, got {w.get_key('AAPL')}"
    assert w.get_key("TSLA") == 0.5, f"Expected: 0.5, got {w.get_key('TSLA')}"


def test_can_clear_position():
    port = setup_portfolio()

    orders = port.recalibrate(Weight({"AAPL": 1}))

    w = port.get_weight()

    assert w.get_key("AAPL") == 1, f"Expected: 1, got {w.get_key('AAPL')}"
    assert len(orders) == 1, f"Expected: 1, got {len(orders)}"
    assert (
        orders[0].stock.symbol == "TSLA"
    ), f"Expected: TSLA, got {orders[0].stock.symbol}"
    assert orders[0].quantity == 100, f"Expected: 100, got {orders[0].quantity}"


if __name__ == "__main__":
    test_can_init_portfolio()
    test_can_get_weights()
    test_can_recalibrate_portfolio()
    test_can_clear_position()
