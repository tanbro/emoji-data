import os
from typing import Iterable, Tuple, Union, TextIO

from pkg_resources import Requirement, resource_filename

from emoji_data import version

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
DATAFILE_TEST = resource_filename(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-test.txt']))
)


def read_data_file_iterable(handle: TextIO) -> Iterable[Tuple[str, str]]:
    for line in handle:
        content = comment = ''
        line = line.strip()
        if not line:
            continue
        if line[0] in '#;':
            continue
        parts = [s.strip() for s in line.split('#', 1)]
        content = parts[0]
        if not content:
            continue
        try:
            comment = parts[1]
        except IndexError:
            pass
        yield content, comment


def code_points_to_string(code_points: Union[int, str, Iterable[int], Iterable[str]]) -> str:
    if isinstance(code_points, str):
        return ''.join(chr(int(s, 16)) for s in code_points.split())
    if isinstance(code_points, int):
        return chr(code_points)
    if isinstance(code_points, Iterable):
        if all(isinstance(m, str) for m in code_points):
            return ''.join(chr(int(s, 16)) for s in code_points)
        if all(isinstance(m, int) for m in code_points):
            return ''.join(chr(n) for n in code_points)
    raise TypeError('Type of argument `code_points` is invalid.')


def code_point_to_regex(code_point: int) -> str:
    if code_point > 0xffff:
        return r'\U{:08X}'.format(code_point)
    else:
        return r'\u{:04X}'.format(code_point)
