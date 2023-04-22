from typing import List
from dataclasses import dataclass
from src.lib.stock import Stock
from src.lib.order import Order, Currency


@dataclass
class Position:
    stock: Stock

    orders: List[Order]

    def __post_init__(self) -> None:
        assert isinstance(self.stock, Stock), "Stock should be Stock type"

        assert (
            len(set(isinstance(order, Order) for order in self.orders)) == 1
        ), "Orders should be Order type"

        assert (
            len(set(self.stock == order.stock for order in self.orders)) == 1
        ), "All orders symbol should be same symbol"

        assert self.get_quantity() > 0, "Quantity must be a positive number"

    def get_quantity(self) -> float | int:
        quantity = 0
        for o in self.orders:
            if o.is_buy():
                quantity += o.quantity
            else:
                quantity -= o.quantity

        return quantity

    def get_avr_buy_price(self, currency: Currency = Currency.GBP) -> float:
        buy_orders = [
            o.get_price_in_currency(currency) for o in self.orders if o.is_buy()
        ]

        return sum(buy_orders) / len(buy_orders)

    def get_total_value(self, currency: Currency = Currency.GBP) -> float:
        return self.get_avr_buy_price(currency) * self.get_quantity()

    def add_order(self, order: Order) -> None:
        if order.is_sell() and self.get_quantity() < order.quantity:
            raise Exception("Insufficient quantity to add sell order")

        self.orders.append(order)
