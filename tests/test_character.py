import unittest

from emoji_data import EmojiCharacter, EmojiCharProperty, code_points_to_string, emoji_data_lines
from emoji_data.definitions import (
    initial_emoji_patterns,
    is_default_emoji_presentation_character,
    is_default_text_presentation_character,
    is_emoji_character,
    is_emoji_component,
    is_emoji_modifier,
    is_emoji_modifier_base,
    is_emoji_presentation_selector,
    is_extended_pictographic_character,
    is_regional_indicator,
    is_text_presentation_selector,
    release_emoji_patterns,
)


class CharacterTestCase(unittest.TestCase):
    test_data = []  # type:ignore[var-annotated]

    @classmethod
    def setUpClass(cls):
        EmojiCharacter.initial()
        initial_emoji_patterns()  # 添加这一行确保模式被初始化
        for content, _ in emoji_data_lines("emoji-test.txt"):
            cls.test_data.append([s.strip() for s in content.split(";", 1)])

    @classmethod
    def tearDownClass(cls):
        release_emoji_patterns()
        EmojiCharacter.release()

    def test_code_points(self):
        for code_points, _ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertTrue(all(ord(c) in EmojiCharacter for c in s))

    def test_character_properties(self):
        # 测试特定字符的属性
        # 测试区域指示符
        regional_indicator_a = EmojiCharacter.from_hex(0x1F1E6)  # 🇦
        self.assertTrue(EmojiCharProperty.ECOMP in regional_indicator_a.properties)
        self.assertTrue(is_regional_indicator(regional_indicator_a.string))

        # 测试emoji呈现选择器
        emoji_pres_selector = EmojiCharacter.from_hex(0xFE0F)
        # VS16 (Emoji Presentation Selector) 不一定有 ECOMP 属性
        self.assertTrue(is_emoji_presentation_selector(emoji_pres_selector.string))

        # 测试文本呈现选择器
        text_pres_selector = EmojiCharacter.from_hex(0xFE0E)
        # VS15 (Text Presentation Selector) 不一定有 ECOMP 属性
        self.assertTrue(is_text_presentation_selector(text_pres_selector.string))

        # 测试emoji修饰符
        emoji_modifier = EmojiCharacter.from_hex(0x1F3FB)  # 🏻 (Light Skin Tone)
        self.assertTrue(EmojiCharProperty.EMOD in emoji_modifier.properties)
        self.assertTrue(is_emoji_modifier(emoji_modifier.string))

        # 测试emoji修饰符基础字符
        emoji_modifier_base = EmojiCharacter.from_hex(0x261D)  # ☝️ (Index Pointing Up)
        self.assertTrue(EmojiCharProperty.EBASE in emoji_modifier_base.properties)
        self.assertTrue(is_emoji_modifier_base(emoji_modifier_base.string))


class CharacterPropertyDefinitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        EmojiCharacter.initial()
        initial_emoji_patterns()

    @classmethod
    def tearDownClass(cls):
        release_emoji_patterns()
        EmojiCharacter.release()

    def test_property_definition(self):
        for c in EmojiCharacter.values():
            if EmojiCharProperty.EMOJI in c.properties:
                self.assertTrue(is_emoji_character(c.string), f"{c=}")
            if EmojiCharProperty.EXTPICT in c.properties:
                self.assertTrue(is_extended_pictographic_character(c.string), f"{c=}")
            if EmojiCharProperty.ECOMP in c.properties:
                self.assertTrue(is_emoji_component(c.string), f"{c=}")
            if EmojiCharProperty.EPRES in c.properties:
                self.assertTrue(is_default_emoji_presentation_character(c.string), f"{c=}")
            if EmojiCharProperty.EPRES not in c.properties:
                self.assertTrue(is_default_text_presentation_character(c.string), f"{c=}")

    def test_specific_character_types(self):
        # 测试特定类型的字符
        # 测试区域指示符
        for code_point in range(0x1F1E6, 0x1F200):  # 区域指示符范围
            if code_point in EmojiCharacter:
                char = EmojiCharacter.from_hex(code_point)
                self.assertTrue(is_regional_indicator(char.string))

        # 测试标签字符
        for code_point in range(0xE0020, 0xE007F):  # 标签字符范围
            if code_point in EmojiCharacter:
                char = EmojiCharacter.from_hex(code_point)
                self.assertTrue(is_emoji_component(char.string))


if __name__ == "__main__":
    unittest.main()
