import os
import unittest
from typing import ClassVar, MutableSequence, Tuple

from emoji_data import (
    EmojiCharacter,
    EmojiCharProperty,
    EmojiSequence,
    QualifiedType,
    code_points_to_string,
    detect_qualified,
    emoji_data_lines,
    is_emoji_flag_sequence,
    is_emoji_keycap_sequence,
    is_emoji_modifier_sequence,
    is_emoji_presentation_sequence,
    is_emoji_zwj_sequence,  # 添加这一行
    load_emoji_data,
    unload_emoji_data,
)


class SequenceTestCase(unittest.TestCase):
    test_data: ClassVar[MutableSequence[Tuple[str, str, str, str, str]]] = []

    @classmethod
    def setUpClass(cls):
        load_emoji_data()
        for content, comment in emoji_data_lines("emoji-test.txt"):
            code_points, qualified = (x.strip() for x in content.split(";", 1))
            s, ver, desc = (x.strip() for x in comment.strip().split(maxsplit=2))
            cls.test_data.append((code_points, qualified, s, ver, desc))

    @classmethod
    def tearDownClass(cls):
        unload_emoji_data()

    def test_length(self):
        for code_points, *_ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertEqual(len(code_points.split()), len(s), f"code_points: {code_points}")

    def test_qualified(self):
        for code_points, status, *_ in self.test_data:
            s = code_points_to_string(code_points)
            if status in ("FQE", "MQE", "UQE"):
                self.assertEqual(
                    detect_qualified(s),
                    QualifiedType(status),
                    f"wrong qualified detected: {s!r}({code_points}, {status})",
                )
            elif status == "component":
                ec = EmojiCharacter.from_character(s)
                self.assertTrue(
                    EmojiCharProperty.ECOMP in ec.properties,
                    f"{ec!r} has no {status}({s!r}<{code_points}>)",
                )

    def test_string(self):
        for code_points, _, s, *_ in self.test_data:
            s_ = code_points_to_string(code_points)
            self.assertEqual(s, s_)

    def test_sequence(self):
        for code_points, status, s, *_ in self.test_data:
            if status == "component":
                continue
            if status != "fully-qualified":
                self.assertNotIn(s, EmojiSequence)
                continue
            em0 = EmojiSequence.from_hex(code_points)
            em1 = EmojiSequence.from_string(s)
            self.assertEqual(em0, em1)
            self.assertEqual(s, em0.string)
            self.assertEqual(code_points, em0.code_points_string)
            self.assertEqual(s, em1.string)
            self.assertEqual(code_points, em1.code_points_string)

    def test_type_field(self):
        """https://unicode.org/reports/tr51/#Emoji_Sets"""
        for code_points, status, *_ in self.test_data:
            if status != "fully-qualified":
                continue
            es = EmojiSequence.from_hex(code_points)
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
                    is_emoji_keycap_sequence(es.string),
                    f"wrong Emoji_Keycap_Sequence type_field detected: {es!r}",
                )
            elif es.type_field == "Emoji_Flag_Sequence":
                self.assertTrue(
                    is_emoji_flag_sequence(es.string),
                    f"wrong Emoji_Flag_Sequence type_field detected: {es!r}",
                )
            elif es.type_field == "Emoji_Modifier_Sequence":
                self.assertTrue(
                    is_emoji_modifier_sequence(es.string),
                    f"wrong Emoji_Modifier_Sequence type_field detected: {es!r}",
                )
            # 添加对ZWJ序列的测试
            elif es.type_field == "RGI_Emoji_ZWJ_Sequence":
                self.assertTrue(
                    is_emoji_zwj_sequence(es.string),
                    f"wrong RGI_Emoji_ZWJ_Sequence type_field detected: {es!r}",
                )


class SequencePatternTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_emoji_data()

    def test_no_emoji(self):
        for s in ("", " ", "\n", "abc", " abc\n bcd"):
            self.assertEqual(len(EmojiSequence.find_all(s)), 0)

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
        emojis = [
            "1F468 200D 1F468 200D 1F467",
            "1F468 200D 1F468 200D 1F467 200D 1F467",
        ]
        s = "".join(code_points_to_string(m) for m in emojis)
        cnt = sum(1 for _ in EmojiSequence.find(s))
        self.assertEqual(cnt, 2)

    # 添加更多测试用例
    def test_emoji_zwj_sequence(self):
        # 测试ZWJ序列，如家庭表情符号
        s = "👨‍👩‍👧"  # 家庭: 男人、女人、女孩
        self.assertTrue(is_emoji_zwj_sequence(s))
        self.assertEqual(len(EmojiSequence.find_all(s)), 1)

    def test_emoji_flag_sequence(self):
        # 测试国旗序列
        s = "🇺🇸"  # 美国国旗
        self.assertTrue(is_emoji_flag_sequence(s))
        self.assertEqual(len(EmojiSequence.find_all(s)), 1)

    def test_emoji_keycap_sequence(self):
        # 测试按键序列
        s = "1️⃣"  # 数字1按键
        self.assertTrue(is_emoji_keycap_sequence(s))
        self.assertEqual(len(EmojiSequence.find_all(s)), 1)

    def test_emoji_modifier_sequence(self):
        # 测试修饰符序列（如肤色）
        s = "👍🏿"  # 深色拇指向上
        self.assertTrue(is_emoji_modifier_sequence(s))
        self.assertEqual(len(EmojiSequence.find_all(s)), 1)

    def test_find_all_with_mixed_emojis(self):
        # 测试在文本中查找所有类型的emoji
        text = "Hello 👨‍👩‍👧 world! 🇺🇸 How are you? 1️⃣ and 👍🏿"
        found_emojis = EmojiSequence.find_all(text)
        self.assertEqual(len(found_emojis), 4)

        # 检查找到的emoji
        emoji_strings = [emoji[0].string for emoji in found_emojis]
        self.assertIn("👨‍👩‍👧", emoji_strings)  # ZWJ序列
        self.assertIn("🇺🇸", emoji_strings)  # 国旗序列
        self.assertIn("1️⃣", emoji_strings)  # 按键序列
        self.assertIn("👍🏿", emoji_strings)  # 修饰符序列


if __name__ == "__main__":
    unittest.main()
