from unittest import TestCase

from emoji_data import EmojiData


class InitialTest(TestCase):

    def setUp(self):
        EmojiData.initial()
        self.pat = EmojiData.get_regex_pattern()
        self.assertIsNotNone(self.pat)

    def test_sub_replace(self):
        txt = self.pat.sub('3', '12☺45')
        self.assertEqual(txt, '12345')
