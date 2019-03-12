import unittest

from emoji_data.sequence import EmojiSequence
from emoji_data.utils import reload_test_data


class SequenceTestCase(unittest.TestCase):
    test_data = []

    @classmethod
    def setUpClass(cls):
        cls.test_data = reload_test_data()
        EmojiSequence.initial()

    def test_code_points(self):
        for code_points, qualified_type in self.test_data:
            if qualified_type == 'fully-qualified':
                EmojiSequence.from_codes(code_points)


if __name__ == '__main__':
    unittest.main()
