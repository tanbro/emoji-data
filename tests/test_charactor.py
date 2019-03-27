import os
import unittest

from pkg_resources import Requirement, resource_filename

from emoji_data import code_points_to_string, is_emoji_character
from emoji_data.utils import read_data_file_iterable

DATAFILE_TEST = resource_filename(
    Requirement.parse('emoji_data'),
    os.path.join('emoji_data', 'data', 'emoji-test.txt')
)


class CharacterTestCase(unittest.TestCase):
    test_data = []

    @classmethod
    def setUpClass(cls):
        with open(DATAFILE_TEST, encoding='utf-8') as fp:
            for content, _ in read_data_file_iterable(fp):
                cls.test_data.append([s.strip() for s in content.split(';', 1)])

    def test_code_points(self):
        for code_points, _ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertTrue(all(is_emoji_character(c) for c in s))


if __name__ == '__main__':
    unittest.main()
