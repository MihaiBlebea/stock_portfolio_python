from typing import List
from dataclasses import dataclass, field
from src.lib.position import Position
from src.lib.order import Order, Currency
from src.lib.stock import Stock


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

    def add_order(self, order: Order) -> Position:
        pos = self.get_position(order.stock.symbol)

        if pos is None:
            assert order.is_buy(), "Insuficient quantity to add sell order"
            pos = Position(order.stock, [order])
            self.positions.append(pos)

            return pos

        pos.add_order(order)

        return pos
