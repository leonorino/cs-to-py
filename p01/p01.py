from decimal import Decimal


class Amount:
    def __init__(self, initial: Decimal):
        if initial < 0:
            raise ValueError("amount must be positive")

        self._balance = initial

    @property
    def balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("amount must be positive")

        self._balance += amount

    def withdraw(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("amount must be positive")

        if amount > self._balance:
            raise ValueError("insufficient funds")

        self._balance -= amount
