from src.lib import Stock, Currency


def test_can_init_stock():
    aapl = Stock("AAPL", 0.56, 10.02, Currency.USD)

    assert aapl.symbol == "AAPL", f"Expected: AAPL, got {aapl.symbol}"
    assert aapl.div_yield == 0.56, f"Expected: 0.56, got {aapl.div_yield}"
    assert aapl.current_price == 10.02, f"Expected: 10.02, got {aapl.current_price}"
    assert aapl.currency == Currency.USD, f"Expected: Currency.USD, got {aapl.currency}"


def test_compare_stocks():
    aapl = Stock("AAPL", 0.56, 10.02, Currency.USD)
    aapl_clone = Stock("AAPL", 0.2, 22.02, Currency.USD)
    tsla = Stock("TSLA", 0, 165.08, Currency.USD)

    assert aapl != tsla, "Expected stocks not to be equal"
    assert aapl == aapl_clone, "Expected stocks to be equal"


if __name__ == "__main__":
    test_can_init_stock()
    test_compare_stocks()
