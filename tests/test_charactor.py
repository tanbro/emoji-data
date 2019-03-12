import unittest

from emoji_data.character import EmojiCharacter
from emoji_data.utils import reload_test_data


class CharacterTestCase(unittest.TestCase):
    test_data = []

    @classmethod
    def setUpClass(cls):
        cls.test_data = reload_test_data()
        EmojiCharacter.initial()

    def test_code_points(self):
        for code_points, _ in self.test_data:
            for code in code_points:
                self.assertTrue(code in EmojiCharacter)


if __name__ == '__main__':
    unittest.main()
