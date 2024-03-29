import os
import unittest

from emoji_data import (
    EmojiCharacter,
    EmojiCharProperty,
    EmojiSequence,
    QualifiedType,
    code_points_to_string,
    data_file,
    detect_qualified,
    is_emoji_flag_sequence,
    is_emoji_keycap_sequence,
    is_emoji_modifier_sequence,
    is_emoji_presentation_sequence,
    read_data_file_iterable,
)


class SequenceTestCase(unittest.TestCase):
    test_data = []

    @classmethod
    def setUpClass(cls):
        with data_file("emoji-test.txt").open(encoding="utf8") as fp:
            for content, _ in read_data_file_iterable(fp):
                cls.test_data.append(tuple(s.strip() for s in content.split(";", 1)))

    def test_length(self):
        for code_points, *_ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertEqual(len(code_points.split()), len(s), f"code_points: {code_points}")

    def test_qualified(self):
        for code_points, status in self.test_data:
            s = code_points_to_string(code_points)
            if status in ("fully-qualified", "minimally-qualified", "unqualified"):
                self.assertEqual(
                    detect_qualified(s), QualifiedType(status), f"wrong qualified detected: {s!r}({code_points}, {status})"
                )
            elif status == "component":
                ec = EmojiCharacter.from_character(s)
                self.assertTrue(EmojiCharProperty.ECOMP in ec.properties, f"{ec!r} has no {status}({s!r}<{code_points}>)")

    def test_type_field(self):
        """https://unicode.org/reports/tr51/#Emoji_Sets"""
        for code_points, *_ in self.test_data:
            try:
                es = EmojiSequence.from_hex(code_points)
            except KeyError:
                pass
            else:
                if es.type_field == "Basic_Emoji":
                    # https://unicode.org/reports/tr51/#def_basic_emoji_set
                    if len(es.characters) > 1:
                        self.assertTrue(
                            is_emoji_presentation_sequence(es.string)
                            and all(EmojiCharProperty.EPRES not in c.properties for c in es.characters),
                            f"wrong Basic_Emoji type_field detected: {es!r}",
                        )
                    else:
                        self.assertTrue(EmojiCharProperty.EPRES in es.characters[0].properties)
                elif es.type_field == "Emoji_Keycap_Sequence":
                    self.assertTrue(
                        is_emoji_keycap_sequence(es.string), f"wrong Emoji_Keycap_Sequence type_field detected: {es!r}"
                    )
                elif es.type_field == "Emoji_Flag_Sequence":
                    self.assertTrue(is_emoji_flag_sequence(es.string), f"wrong Emoji_Flag_Sequence type_field detected: {es!r}")
                elif es.type_field == "Emoji_Modifier_Sequence":
                    self.assertTrue(
                        is_emoji_modifier_sequence(es.string), f"wrong Emoji_Modifier_Sequence type_field detected: {es!r}"
                    )


class SequencePatternTestCase(unittest.TestCase):
    def test_no_emoji(self):
        for s in ("", " ", "\n", "abc", " abc\n bcd"):
            self.assertListEqual(EmojiSequence.find_all(s), [])

    def test_single_one_char_emoji(self):
        s = "😀"
        self.assertListEqual([m.string for m, _, _ in EmojiSequence.find_all(s)], [s])

    def test_one_char_emoji_started_text(self):
        s = "😀笑脸"
        self.assertIsNotNone(EmojiSequence.pattern.match(s))
        self.assertIsNotNone(EmojiSequence.pattern.search(s))

    def test_1char_emoji_in_text(self):
        s = "这是😀笑脸"
        self.assertIsNone(EmojiSequence.pattern.match(s))
        _, p0, p1 = EmojiSequence.find_all(s)[0]
        self.assertEqual((p0, p1), (2, 3))

    def test_many_one_char_emoji_in_text(self):
        s = "1😛 2😛 3😛"
        cnt = 0
        cnt = sum(1 for _ in EmojiSequence.find(s))
        self.assertEqual(cnt, 3)

    def test_single_multi_chars_emoji(self):
        s = "☺️"
        self.assertEqual(len(s), 2)
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_single_multichars_emoji_started_text(self):
        s = "☺️ 也是笑脸"
        self.assertIsNotNone(EmojiSequence.pattern.match(s))

    def test_single_multi_chars_emoji_in_text(self):
        s = "这个☺️也是笑脸"
        self.assertIsNone(EmojiSequence.pattern.match(s))
        _, p0, p1 = EmojiSequence.find_all(s)[0]
        self.assertEqual((p0, p1), (2, 4))

    def test_many_multi_chars_emoji_in_text(self):
        s = "1☺️ 2☺️ 3☺️"
        cnt = sum(1 for _ in EmojiSequence.find(s))
        self.assertEqual(cnt, 3)

    def test_many_multi_chars_emoji_in_multiline_text(self):
        s = "1☺️ {0}2☺️ {0}3☺️".format(os.linesep)
        cnt = sum(1 for _ in EmojiSequence.find(s))
        self.assertEqual(cnt, 3)

    def test_continues_two_with_same_start_part(self):
        emojis = ["1F468 200D 1F468 200D 1F467", "1F468 200D 1F468 200D 1F467 200D 1F467"]
        s = "".join(code_points_to_string(m) for m in emojis)
        cnt = sum(1 for _ in EmojiSequence.find(s))
        self.assertEqual(cnt, 2)


if __name__ == "__main__":
    unittest.main()
