import ast
import threading
from datetime import datetime
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


def is_absolute_import_that_doesnt_reference_macros(
    node: ast.stmt, generated_name: str
) -> bool:
    return (
        isinstance(node, ast.ImportFrom)
        and node.level == 0
        and not (
            "__macro__.types" in ast.unparse(node)
            and generated_name in [alias.name for alias in node.names]
        )
    ) or isinstance(node, ast.Import)


def debounce[**P](delay: float) -> Callable[[Callable[P, None]], Callable[P, None]]:
    def _debounce(func: Callable[P, None]) -> Callable[P, None]:
        last_call_time: dict[tuple[Any, ...], datetime] = {}

        def flush(called_at: datetime, *args: P.args, **kwargs: P.kwargs) -> None:
            nonlocal last_call_time
            if last_call_time[tuple(args)] > called_at:
                return  # no-op
            func(*args, **kwargs)

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
            assert not kwargs, "kwargs are not supported by debounce"
            last_call_time[tuple(args)] = datetime.now()
            threading.Timer(delay, flush, args=(datetime.now(), *args)).start()

        return wrapper

    return _debounce
