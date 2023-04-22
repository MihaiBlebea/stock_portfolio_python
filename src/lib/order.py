from __future__ import annotations
from dataclasses import dataclass
from abc import abstractmethod
from enum import Enum
from currency_converter import CurrencyConverter
from src.lib.stock import Stock, Currency


class Direction(Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass
class Order:
    stock: Stock

    price: float

    currency: Currency

    quantity: float | int

    direction: Direction

    def __post_init__(self) -> None:
        assert isinstance(self.stock, Stock), "Stock should be Stock type"
        assert isinstance(self.price, float), "Price should be float type"
        assert isinstance(self.currency, Currency), "Currency should Currency type"
        assert isinstance(
            self.quantity, (int, float)
        ), "Quantity should be int or float type"

    @abstractmethod
    def buy(
        stock: Stock, price: float, currency: Currency, quantity: float | int
    ) -> Order:
        return Order(stock, price, currency, quantity, Direction.BUY)

    @abstractmethod
    def sell(
        stock: Stock, price: float, currency: Currency, quantity: float | int
    ) -> Order:
        return Order(stock, price, currency, quantity, Direction.SELL)

    def is_buy(self) -> bool:
        return self.direction == Direction.BUY

    def is_sell(self) -> bool:
        return self.direction == Direction.SELL

    def get_price_in_currency(self, currency: Currency = Currency.GBP) -> float:
        if self.currency == currency:
            return self.price

        c = CurrencyConverter()

        return c.convert(self.price, self.currency.value, currency.value)
