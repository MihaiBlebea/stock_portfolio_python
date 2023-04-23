from typing import List
from src.lib import Portfolio, Stock, Position, Order, Currency
from src.weight import Weight


class SmartPortfolio(Portfolio):
    def __init__(self, positions: List[Position], currency: Currency = Currency.GBP):
        super().__init__(positions, currency)

    def get_weight(self) -> Weight:
        weight = Weight()
        total_value = self.get_total_value(self.currency)

        for pos in self.positions:
            weight.set_value(
                pos.stock.symbol, pos.get_total_value(self.currency) / total_value
            )

        return weight

    def add_calibrated_position(self, stock: Stock, weight: float) -> Position:
        assert isinstance(stock, Stock), "Stock should be Stock type"
        assert isinstance(weight, float), "Weight should be float type"
        assert self.get_position(stock.symbol) is None, "Position already exists"

        total_value = self.get_total_value(self.currency)
        quantity = total_value * weight / stock.get_price_in_currency(self.currency)
        pos = Position(
            stock, [Order.buy(stock, stock.current_price, stock.currency, quantity)]
        )
        self.positions.append(pos)

        return pos

    def recalibrate(self, weight: Weight, dry_run: bool = True) -> List[Order]:
        assert isinstance(weight, Weight), "Weight must be Weight type"

        orders = []

        # if position not in weight, just sell everything
        for w in self.get_weight().keys():
            if w not in weight.keys():
                pos = self.get_position(w)
                order = Order.sell(
                    pos.stock,
                    pos.stock.get_price_in_currency(self.currency),
                    self.currency,
                    pos.get_quantity(),
                )
                orders.append(order)
                self.add_order(order)

        # if position not the correct weight, create orders to recalibrate
        for w in weight.keys():
            assert (
                w in self.get_weight().keys()
            ), "Symbol is not part of the portfolio yet"

            current_weight = self.get_weight()
            total_value = self.get_total_value(self.currency)

            pos = self.get_position(w)
            diff_amount = (
                abs(current_weight.get_key(w) - weight.get_key(w)) * total_value
            )
            quantity = diff_amount / pos.stock.get_price_in_currency(self.currency)

            if current_weight.get_key(w) > weight.get_key(w):
                # create sell order
                order = Order.sell(
                    pos.stock,
                    pos.stock.get_price_in_currency(self.currency),
                    self.currency,
                    quantity,
                )
                orders.append(order)
                self.add_order(order)

            elif current_weight.get_key(w) < weight.get_key(w):
                # create buy orders
                order = Order.buy(
                    pos.stock,
                    pos.stock.get_price_in_currency(self.currency),
                    self.currency,
                    quantity,
                )
                orders.append(order)
                self.add_order(order)

        return orders
