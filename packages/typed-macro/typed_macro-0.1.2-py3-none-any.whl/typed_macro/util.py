import ast
from typing import Any, Callable, Iterable


def one_or_none[T](it: Iterable[T]) -> T | None:
    iterator = iter(it)
    first = next(iterator, None)

    class Sentinel:
        pass

    SENTINEL = Sentinel()
    assert (
        next(iterator, SENTINEL) is SENTINEL
    ), "found more than one result when one or none was expected"
    return first


def first_or_none[T](it: Iterable[T]) -> T | None:
    return next(iter(it), None)


def get_file_pos_from_line_col(lineno: int, col_offset: int, file_contents: str) -> int:
    lineno -= 1  # adjust for zero-index
    # (weirdly, col_offset is already zero-indexed by ast library)
    lines = file_contents.splitlines(keepends=True)
    return sum(len(line) for line in lines[:lineno]) + col_offset


def get_generated_name(func_or_class: Callable[..., Any] | type) -> str:
    if isinstance(func_or_class, type):
        return f"Gen{func_or_class.__name__}"
    else:
        return f"gen_{func_or_class.__name__}"


def is_absolute_import(node: ast.stmt) -> bool:
    return (isinstance(node, ast.ImportFrom) and node.level == 0) or isinstance(
        node, ast.Import
    )
