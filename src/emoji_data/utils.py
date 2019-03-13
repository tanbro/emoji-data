import os
from typing import BinaryIO, Iterator

from pkg_resources import Requirement, resource_stream

from emoji_data import version

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
TEST_DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-test.txt']))
)


def read_data_file_stream_iterable(handle: BinaryIO) -> Iterator[str]:
    for line_bytes in handle:
        line_text = ''
        line_bytes = line_bytes.strip()
        if line_bytes:
            if line_bytes[0] not in b'#;':
                line_text = line_bytes.decode('utf-8').split('#', 1)[0].strip()
        yield line_text


def reload_test_data():
    result = []
    TEST_DATAFILE_STREAM.seek(0)
    for line in read_data_file_stream_iterable(TEST_DATAFILE_STREAM):
        if not line:
            continue
        line = line.split('#', 1)[0].strip()
        code_points, qualified_type = (part.strip() for part in line.split(';', 1))
        result.append((
            [int(s, 16) for s in code_points.split()],
            qualified_type
        ))
    return result


class BaseDictContainer(type):
    def __new__(mcs, name, bases, attrs):  # pylint:disable=bad-mcs-classmethod-argument
        mcs._data = dict()
        return super().__new__(mcs, name, bases, attrs)

    def __setitem__(self, key, value):  # pylint: disable=C0203
        self._data[key] = value

    def __delitem__(self, key):  # pylint: disable=C0203
        del self._data[key]

    def __getitem__(self, key):  # pylint: disable=C0203
        return self._data[key]

    def __contains__(self, key):  # pylint: disable=C0203
        return key in self._data

    def __iter__(self):  # pylint: disable=bad-mcs-method-argument
        for k, v in self._data.items():  # pylint: disable=invalid-name
            yield k, v

    def __len__(self):  # pylint: disable=C0203
        return len(self._data)
