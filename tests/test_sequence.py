import os
import unittest

from pkg_resources import Requirement, resource_filename

from emoji_data import (EmojiSequence, QualifiedType, code_points_to_string,
                        detect_qualified, is_emoji_character,
                        is_emoji_flag_sequence, is_emoji_keycap_sequence,
                        is_emoji_modifier_sequence)
from emoji_data.utils import read_data_file_iterable

DATAFILE_TEST = resource_filename(
    Requirement.parse('emoji_data'),
    os.path.join('emoji_data', 'data', 'emoji-test.txt')
)


class SequenceTestCase(unittest.TestCase):
    test_data = []

    @classmethod
    def setUpClass(cls):
        with open(DATAFILE_TEST, encoding='utf-8') as fp:
            for content, _ in read_data_file_iterable(fp):
                cls.test_data.append([s.strip() for s in content.split(';', 1)])

    def test_status(self):
        for code_points, status in self.test_data:
            obj = EmojiSequence.from_hex(code_points)
            s = obj.string
            self.assertEqual(obj.status, status)
            if obj.type_field:
                self.assertEqual(detect_qualified(s), QualifiedType(status))

    def test_type_field(self):
        for code_points, _ in self.test_data:
            obj = EmojiSequence.from_hex(code_points)  # type: EmojiSequence
            s = obj.string
            if obj.type_field == 'Basic_Emoji':
                self.assertTrue(is_emoji_character(s))
            elif obj.type_field == 'Emoji_Keycap_Sequence':
                self.assertTrue(is_emoji_keycap_sequence(s))
            elif obj.type_field == 'Emoji_Flag_Sequence':
                self.assertTrue(is_emoji_flag_sequence(s))
            elif obj.type_field == 'Emoji_Modifier_Sequence':
                self.assertTrue(is_emoji_modifier_sequence(s))


class SequencePatternTestCase(unittest.TestCase):
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

    def test_single_multichar_emoji(self):
        s = '☺️'
        self.assertEqual(len(s), 2)
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_single_multichar_emoji_started_text(self):
        s = '☺️ 也是笑脸'
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_single_multichar_emoji_in_text(self):
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

    def test_continues_two_with_same_start_part(self):
        emojis = [
            '1F468 200D 1F468 200D 1F467',
            '1F468 200D 1F468 200D 1F467 200D 1F467'
        ]
        s = ''.join(code_points_to_string(m) for m in emojis)
        cnt = 0
        m = EmojiSequence.pattern.search(s)
        while m:
            cnt += 1
            m = EmojiSequence.pattern.search(s, m.end())
        self.assertEqual(cnt, 2)


if __name__ == '__main__':
    unittest.main()
