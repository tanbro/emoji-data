import os
import unittest

from pkg_resources import Requirement, resource_filename

from emoji_data import (EmojiCharacter, EmojiSequence, QualifiedType, code_points_to_string,
                        detect_qualified, is_emoji_character,
                        is_emoji_flag_sequence, is_emoji_keycap_sequence,
                        is_emoji_modifier_sequence)
from emoji_data.utils import read_data_file_iterable

DATAFILE_TEST = resource_filename(
    Requirement.parse('emoji_data'),
    os.path.join('emoji_data', 'data', 'emoji-test.txt')
)


class SequenceTestCase(unittest.TestCase):
    test_data = []  # type: list[tuple[str,str]]

    @classmethod
    def setUpClass(cls):
        with open(DATAFILE_TEST, encoding='utf-8') as fp:
            for content, _ in read_data_file_iterable(fp):
                cls.test_data.append(tuple(s.strip() for s in content.split(';', 1)))  # type: ignore

    def setUp(self):
        EmojiCharacter.initial()
        EmojiSequence.initial()

    def tearDown(self):
        EmojiSequence.release()
        EmojiCharacter.release()

    def test_len(self):
        for code_points, *_ in self.test_data:
            obj = EmojiSequence.from_hex(code_points)
            self.assertEqual(len(code_points.split()), len(obj))

    def test_status(self):
        for code_points, status in self.test_data:
            obj = EmojiSequence.from_hex(code_points)
            s = obj.string
            self.assertEqual(obj.status, status)
            if obj.type_field:
                self.assertEqual(detect_qualified(s), QualifiedType(status))

    def test_type_field(self):
        for code_points, *_ in self.test_data:
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
            self.assertListEqual(EmojiSequence.find(s), [])

    def test_single_one_char_emoji(self):
        s = '😀'
        self.assertListEqual(
            [m.string for m, _, _ in EmojiSequence.find(s)],
            [s]
        )

    def test_one_char_emoji_started_text(self):
        s = '😀笑脸'
        self.assertIsNotNone(EmojiSequence.pattern.match(s))
        self.assertIsNotNone(EmojiSequence.pattern.search(s))

    def test_1char_emoji_in_text(self):
        s = '这是😀笑脸'
        self.assertIsNone(EmojiSequence.pattern.match(s))
        e, p0, p1 = EmojiSequence.find(s)[0]
        self.assertEqual((p0, p1), (2, 3))

    def test_many_one_char_emoji_in_text(self):
        s = '1😛 2😛 3😛'
        cnt = 0
        cnt = sum(1 for _ in EmojiSequence.iter_find(s))
        self.assertEqual(cnt, 3)

    def test_single_multi_chars_emoji(self):
        s = '☺️'
        self.assertEqual(len(s), 2)
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_single_multichars_emoji_started_text(self):
        s = '☺️ 也是笑脸'
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_single_multi_chars_emoji_in_text(self):
        s = '这个☺️也是笑脸'
        self.assertIsNone(EmojiSequence.pattern.match(s))
        e, p0, p1 = EmojiSequence.find(s)[0]
        self.assertEqual((p0, p1), (2, 4))

    def test_many_multi_chars_emoji_in_text(self):
        s = '1☺️ 2☺️ 3☺️'
        cnt = sum(1 for _ in EmojiSequence.iter_find(s))
        self.assertEqual(cnt, 3)

    def test_many_multi_chars_emoji_in_multiline_text(self):
        s = '1☺️ {0}2☺️ {0}3☺️'.format(os.linesep)
        cnt = sum(1 for _ in EmojiSequence.iter_find(s))
        self.assertEqual(cnt, 3)

    def test_continues_two_with_same_start_part(self):
        emojis = [
            '1F468 200D 1F468 200D 1F467',
            '1F468 200D 1F468 200D 1F467 200D 1F467'
        ]
        s = ''.join(code_points_to_string(m) for m in emojis)
        cnt = sum(1 for _ in EmojiSequence.iter_find(s))
        self.assertEqual(cnt, 2)


if __name__ == '__main__':
    unittest.main()
