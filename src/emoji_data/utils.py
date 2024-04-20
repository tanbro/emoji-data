from __future__ import annotations

import sys
from typing import Union, TextIO

if sys.version_info < (3, 9):  # pragma: no cover
    from typing import Generator, Iterable, Tuple
    from importlib_resources import files
else:  # pragma: no cover
    from collections.abc import Generator, Iterable
    from importlib.resources import files


__all__ = ["code_points_to_string", "code_point_to_regex", "data_file", "read_data_file_iterable"]


def data_file(file):
    return files(__package__).joinpath("data").joinpath(file)


def _read_data_file_iterable(handle: TextIO):
    for line in handle:
        line = line.strip()
        if not line:
            continue
        if line[0] in "#;":
            continue
        parts = [s.strip() for s in line.split("#", 1)]
        content = parts[0]
        try:
            comment = parts[1]
        except IndexError:
            comment = ""
        yield content, comment


if sys.version_info < (3, 9):

    def read_data_file_iterable(handle) -> Generator[Tuple[str, str], None, None]:
        yield from _read_data_file_iterable(handle)

else:

    def read_data_file_iterable(handle) -> Generator[tuple[str, str], None, None]:
        yield from _read_data_file_iterable(handle)


def code_points_to_string(code_points: Union[int, str, Iterable[int], Iterable[str]]) -> str:
    if isinstance(code_points, str):
        return "".join(chr(int(s, 16)) for s in code_points.split())
    if isinstance(code_points, Iterable):
        return "".join(chr(int(n, 16)) if isinstance(n, str) else chr(n) for n in code_points)
    return chr(code_points)


def code_point_to_regex(code_point: int) -> str:
    return rf"\U{code_point:08X}" if code_point > 0xFFFF else rf"\u{code_point:04X}"
