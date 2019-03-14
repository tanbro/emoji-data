import os
from typing import BinaryIO, Iterator, Tuple

from pkg_resources import Requirement, resource_stream

from emoji_data import version

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
TEST_DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-test.txt']))
)


def read_data_file_iterable(handle: BinaryIO) -> Iterator[Tuple[str, str]]:
    for line_bytes in handle:
        content = ''
        comment = ''
        line_bytes = line_bytes.strip()
        if line_bytes:
            if line_bytes[0] not in b'#;':
                parts = [s.strip() for s in line_bytes.decode('utf-8').split('#', 1)]
                content = parts[0]
                if len(parts):
                    comment = parts[1]
        yield content, comment


def reload_test_data():
    result = []
    TEST_DATAFILE_STREAM.seek(0)
    for content, _ in read_data_file_iterable(TEST_DATAFILE_STREAM):
        if not content:
            continue
        code_points, qualified_type = (part.strip() for part in content.split(';', 1))
        result.append((
            [int(s, 16) for s in code_points.split()],
            qualified_type
        ))
    return result
