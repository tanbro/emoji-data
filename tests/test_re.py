import os
import unittest

from emoji_data.sequence import EmojiSequence


class SequenceRegexTestCase(unittest.TestCase):
    test_data = []

    @classmethod
    def setUpClass(cls):
        EmojiSequence.initial()

    def test_no_emoji(self):
        for s in (
                '',
                ' ',
                '\n',
                'abc',
                ' abc\n bcd'
        ):
            self.assertIsNone(EmojiSequence.pattern.match(s))

    def test_single_1char_emoji(self):
        s = '😀'
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_1char_emoji_started_text(self):
        s = '😀笑脸'
        self.assertIsNotNone(EmojiSequence.pattern.match(s))
        self.assertIsNotNone(EmojiSequence.pattern.search(s))

    def test_1char_emoji_in_text(self):
        s = '这是😀笑脸'
        self.assertIsNone(EmojiSequence.pattern.match(s))
        m = EmojiSequence.pattern.search(s)
        self.assertIsNotNone(m)
        self.assertEqual(m.span(), (2, 3))

    def test_many_1char_emoji_in_text(self):
        s = '1😛 2😛 3😛'
        cnt = 0
        m = EmojiSequence.pattern.search(s)
        while m:
            cnt += 1
            m = EmojiSequence.pattern.search(s, m.end())
        self.assertEqual(cnt, 3)

    def test_sigle_multichar_emoji(self):
        s = '☺️'
        self.assertEqual(len(s), 2)
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_sigle_multichar_emoji_started_text(self):
        s = '☺️ 也是笑脸'
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_sigle_multichar_emoji_in_text(self):
        s = '这个☺️也是笑脸'
        self.assertIsNone(EmojiSequence.pattern.match(s))
        m = EmojiSequence.pattern.search(s)
        self.assertIsNotNone(m)
        self.assertEqual(m.span(), (2, 4))

    def test_many_multichar_emoji_in_text(self):
        s = '1☺️ 2☺️ 3☺️'
        cnt = 0
        m = EmojiSequence.pattern.search(s)
        while m:
            cnt += 1
            m = EmojiSequence.pattern.search(s, m.end())
        self.assertEqual(cnt, 3)

    def test_many_multichar_emoji_in_multiline_text(self):
        s = '1☺️ {0}2☺️ {0}3☺️'.format(os.linesep)
        cnt = 0
        m = EmojiSequence.pattern.search(s)
        while m:
            cnt += 1
            m = EmojiSequence.pattern.search(s, m.end())
        self.assertEqual(cnt, 3)


if __name__ == '__main__':
    unittest.main()
