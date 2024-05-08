import unittest

from emoji_data import EmojiCharacter, code_points_to_string
from emoji_data.utils import emoji_data_lines


class CharacterTestCase(unittest.TestCase):
    test_data = []  # type:ignore[var-annotated]

    @classmethod
    def setUpClass(cls):
        for content, _ in emoji_data_lines("emoji-test.txt"):
            cls.test_data.append([s.strip() for s in content.split(";", 1)])

    def test_code_points(self):
        for code_points, _ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertTrue(all(ord(c) in EmojiCharacter for c in s))


if __name__ == "__main__":
    unittest.main()
