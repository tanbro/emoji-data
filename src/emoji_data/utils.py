import os

from pkg_resources import Requirement, resource_stream

from emoji_data import version

PACKAGE = '.'.join(version.__name__.split('.')[:-1])
TEST_DATAFILE_STREAM = resource_stream(
    Requirement.parse(PACKAGE),
    os.path.join(*(PACKAGE.split('.') + ['data', 'emoji-test.txt']))
)


def reload_test_data():
    result = []
    TEST_DATAFILE_STREAM.seek(0)
    for line in TEST_DATAFILE_STREAM:
        line = line.strip()
        if not line:
            continue
        line = line.decode('utf-8')
        if line[0] in ('#', ';'):
            continue
        line = line.split('#', 1)[0].strip()
        code_points, qualified_type = (part.strip() for part in line.split(';', 1))
        result.append((
            [int(s, 16) for s in code_points.split()],
            qualified_type
        ))
    return result
