from collections.abc import Callable, Iterable
from datetime import date
from decimal import Decimal


Block = Callable[[], str]


def build_report(*blocks: Block) -> str:
    return "".join(block() for block in blocks)


def sales_parts(rows: Iterable[tuple[date, Decimal]]) -> tuple[Block, Block, Block, Block]:
    saved_rows = tuple(rows)

    def header() -> str:
        return "sales\n"

    def row_lines() -> str:
        return "".join(f"{row_date}: {amount}\n" for row_date, amount in saved_rows)

    def footer() -> str:
        return ""

    def summary() -> str:
        return f"rows: {len(saved_rows)}\n"

    return header, row_lines, footer, summary
