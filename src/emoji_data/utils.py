from __future__ import annotations

import sys
from typing import Union, Generator, Iterable, Tuple

if sys.version_info < (3, 9):  # pragma: no cover
    import importlib_resources
else:  # pragma: no cover
    import importlib.resources as importlib_resources


__all__ = ["code_points_to_string", "code_point_to_regex", "emoji_data_lines"]


def emoji_data_lines(data_file: str) -> Generator[Tuple[str, str], None, None]:
    ft = importlib_resources.files(__package__).joinpath("data").joinpath(data_file)
    for line in ft.read_text("utf-8").splitlines():
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
        yield content.strip(), comment.strip()


def code_points_to_string(code_points: Union[int, str, Iterable[Union[int, str]]]) -> str:
    if isinstance(code_points, str):
        return "".join(chr(int(s, 16)) for s in code_points.split())
    if isinstance(code_points, Iterable):
        return "".join(chr(int(n, 16)) if isinstance(n, str) else chr(n) for n in code_points)
    return chr(code_points)


def code_point_to_regex(code_point: int) -> str:
    return rf"\U{code_point:08X}" if code_point > 0xFFFF else rf"\u{code_point:04X}"
