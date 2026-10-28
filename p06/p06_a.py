from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import date
from decimal import Decimal


class Report(ABC):
    def build(self) -> str:
        parts = [self.header(), *self.rows(), self.footer()]
        return "".join(parts)

    @abstractmethod
    def header(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def rows(self) -> Iterable[str]:
        raise NotImplementedError

    def footer(self) -> str:
        return ""


class SalesReport(Report):
    def __init__(self, rows: Iterable[tuple[date, Decimal]]) -> None:
        self._rows = tuple(rows)

    def header(self) -> str:
        return "sales\n"

    def rows(self) -> Iterable[str]:
        return (f"{row_date}: {amount}\n" for row_date, amount in self._rows)


if __name__ == "__main__":
    report = SalesReport([(date(2026, 10, 28), Decimal("125.50"))])
    print(report.build(), end="")
