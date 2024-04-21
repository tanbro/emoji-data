import unittest

from emoji_data import code_points_to_string, EmojiCharacter
from emoji_data.utils import data_file, read_data_file_iterable


class CharacterTestCase(unittest.TestCase):
    test_data = []  # type:ignore[var-annotated]

    @classmethod
    def setUpClass(cls):
        with data_file("emoji-test.txt").open(encoding="utf8") as fp:
            for content, _ in read_data_file_iterable(fp):
                cls.test_data.append([s.strip() for s in content.split(";", 1)])

    def test_code_points(self):
        for code_points, _ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertTrue(all(ord(c) in EmojiCharacter for c in s))


if __name__ == "__main__":
    unittest.main()
