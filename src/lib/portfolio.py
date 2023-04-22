from typing import List, Dict
from dataclasses import dataclass, field
from src.lib.position import Position
from src.lib.order import Order, Currency


@dataclass
class Portfolio:
    positions: List[Position]

    currency: Currency = field(default=Currency.GBP)

    def __post_init__(self) -> None:
        assert (
            len(set(isinstance(p, Position) for p in self.positions)) == 1
        ), "All positions must be Position type"

        assert len(set(pos.stock.symbol for pos in self.positions)) == len(
            self.positions
        ), "No duplicate positions allowed"

    def get_total_value(self, currency: Currency = Currency.GBP) -> float:
        return sum(pos.get_total_value(currency) for pos in self.positions)

    def get_position(self, symbol: str) -> Position | None:
        positions = [
            pos for pos in self.positions if pos.stock.symbol == symbol.upper()
        ]
        if len(positions) == 0:
            return None

        return positions[0]

    def get_weight(self) -> Dict[str, float]:
        weight = {}
        total_value = self.get_total_value(self.currency)

        for pos in self.positions:
            weight[pos.stock.symbol] = pos.get_total_value(self.currency) / total_value

        return weight

    def add_order(self, order: Order) -> Position:
        pos = self.get_position(order.stock.symbol)
        if pos is None:
            assert order.is_buy(), "Insuficient quantity to add sell order"
            pos = Position(order.stock, [order])
            self.positions.append(pos)

        pos.add_order(order)

        return pos

    def recalibrate(
        self, weight: Dict[str, float], dry_run: bool = True
    ) -> List[Order]:
        current_weight = self.get_weight()
        total_value = self.get_total_value(self.currency)

        orders = []
        # if position not the correct weight, create orders to recalibrate
        for w in list(self.get_weight().keys()):
            # if position not in weight, just sell everything
            if w not in weight:
                pos = self.get_position(w)
                orders.append(
                    Order.sell(
                        pos.stock,
                        pos.stock.get_price_in_currency(self.currency),
                        self.currency,
                        pos.get_quantity(),
                    )
                )
                continue

            if current_weight[w] > weight[w]:
                print(f"Selling some {w}")
                # create sell order
                diff_amount = (current_weight[w] - weight[w]) * total_value
                pos = self.get_position(w)
                orders.append(
                    Order.sell(
                        pos.stock,
                        pos.stock.get_price_in_currency(self.currency),
                        self.currency,
                        diff_amount / pos.stock.get_price_in_currency(self.currency),
                    )
                )

            elif current_weight[w] < weight[w]:
                print(f"Buying some {w}")
                # create buy orders
                diff_amount = (weight[w] - current_weight[w]) * total_value
                pos = self.get_position(w)
                orders.append(
                    Order.buy(
                        pos.stock,
                        pos.stock.get_price_in_currency(self.currency),
                        self.currency,
                        diff_amount / pos.stock.get_price_in_currency(self.currency),
                    )
                )

            else:
                # do nothing
                pass

        if dry_run == False:
            for order in orders:
                self.add_order(order)

        return orders
