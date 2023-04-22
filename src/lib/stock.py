from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from currency_converter import CurrencyConverter


class Currency(Enum):
    USD = "USD"
    GBP = "GBP"


@dataclass
class Stock:
    symbol: str

    div_yield: float

    current_price: float

    currency: Currency

    def __post_init__(self) -> None:
        assert isinstance(self.symbol, str), "Symbol should be a string type"
        assert isinstance(
            self.div_yield, (float, int)
        ), "DivYield should be a int or float type"
        assert isinstance(
            self.current_price, float
        ), "CurrentPrice should be a float type"
        assert isinstance(self.currency, Currency), "Currency should be a Currency type"

        self.symbol = self.symbol.upper()

    def __eq__(self, stock: Stock) -> bool:
        return self.symbol == stock.symbol

    def get_price_in_currency(self, currency: Currency) -> float:
        assert isinstance(currency, Currency), "Currency should be a Currency type"
        c = CurrencyConverter()

        return c.convert(self.current_price, self.currency.value, currency.value)
