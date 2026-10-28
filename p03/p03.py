from types import TracebackType
from typing import Optional, TextIO


class ReportWriter:
    def __init__(self, path: str) -> None:
        self._writer: TextIO = open(path, "w", encoding="utf-8")

    def __enter__(self) -> "ReportWriter":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        self._writer.close()
        return False

    def write(self, line: str) -> None:
        self._writer.write(line + "\n")


if __name__ == "__main__":
    with ReportWriter("report.txt") as writer:
        writer.write("header")
        writer.write("body")
