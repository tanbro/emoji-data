import importlib.resources
import unittest

from emoji_data import code_points_to_string, is_emoji_character
from emoji_data.utils import read_data_file_iterable


class CharacterTestCase(unittest.TestCase):
    test_data = []

    @classmethod
    def setUpClass(cls):
        with importlib.resources.open_text('emoji_data.data', 'emoji-test.txt') as fp:
            for content, _ in read_data_file_iterable(fp):
                cls.test_data.append([s.strip() for s in content.split(';', 1)])

    def test_code_points(self):
        for code_points, _ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertTrue(all(is_emoji_character(c) for c in s))


if __name__ == '__main__':
    unittest.main()
