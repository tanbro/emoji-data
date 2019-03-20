from typing import Iterable, TextIO, Tuple, Union


def read_data_file_iterable(handle: TextIO) -> Iterable[Tuple[str, str]]:
    for line in handle:
        line = line.strip()
        if not line:
            continue
        if line[0] in '#;':
            continue
        parts = [s.strip() for s in line.split('#', 1)]
        content = parts[0]
        try:
            comment = parts[1]
        except IndexError:
            comment = ''
        yield content, comment


def code_points_to_string(code_points: Union[int, str, Iterable[int], Iterable[str]]) -> str:
    if isinstance(code_points, str):
        return ''.join(chr(int(s, 16)) for s in code_points.split())
    if isinstance(code_points, Iterable):
        return ''.join(chr(int(n, 16)) if isinstance(n, str) else chr(n) for n in code_points)
    return chr(code_points)


def code_point_to_regex(code_point: int) -> str:
    if code_point > 0xffff:
        return r'\U{:08X}'.format(code_point)
    return r'\u{:04X}'.format(code_point)
