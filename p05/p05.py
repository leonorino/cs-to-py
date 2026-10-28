from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.currency is None:
            raise ValueError("currency must not be None")

    def __add__(self, other: object) -> Any:
        if not isinstance(other, Money):
            return NotImplemented
        
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        
        return Money(self.amount + other.amount, self.currency)


class EqOnlyMoney:
    def __init__(self, amount: Decimal, currency: str) -> None:
        self.amount = amount
        self.currency = currency

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, EqOnlyMoney)
            and self.amount == other.amount
            and self.currency == other.currency
        )


if __name__ == "__main__":
    ten_dollars = Money(Decimal("10.00"), "USD")
    five_dollars = Money(Decimal("5.50"), "USD")
    euros = Money(Decimal("2.00"), "EUR")

    print(ten_dollars + five_dollars)

    try:
        print(ten_dollars + euros)
    except ValueError as error:
        print(f"{type(error).__name__}: {error}")

    prices = {ten_dollars: "ten dollars"}
    print(prices[Money(Decimal("10.00"), "USD")])

    eq_only = EqOnlyMoney(Decimal("10.00"), "USD")
    print(f"EqOnlyMoney.__hash__: {eq_only.__hash__}")
    
    try:
        {eq_only: "ten dollars"}
    except TypeError:
        print("TypeError: EqOnlyMoney is unhashable")
