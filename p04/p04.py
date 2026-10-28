from collections.abc import Callable


class ImportException(Exception):
    pass


def import_file(
    path: str,
    parse: Callable[[list[str]], None],
    retry: Callable[[str], None],
) -> None:
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        parse(lines)
    except PermissionError:
        retry(path)
    except OSError as error:
        raise ImportException(f"cannot read {path}") from error
