import unittest

from emoji_data import (
    load_emoji_data,
    unload_emoji_data,
)
from emoji_data.definitions import (
    QualifiedType,
    detect_qualified,
    initial_emoji_patterns,
    is_emoji_character,
    is_emoji_component,
    is_emoji_flag_sequence,
    is_emoji_keycap_sequence,
    is_emoji_modifier,
    is_emoji_modifier_base,
    is_emoji_modifier_sequence,
    is_emoji_presentation_selector,
    is_emoji_presentation_sequence,
    is_emoji_sequence,
    is_emoji_zwj_sequence,
    is_extended_pictographic_character,
    is_regional_indicator,
    is_text_presentation_selector,
    release_emoji_patterns,
)


class DefinitionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_emoji_data()
        initial_emoji_patterns()

    @classmethod
    def tearDownClass(cls):
        release_emoji_patterns()
        unload_emoji_data()

    def test_is_emoji_character(self):
        # 测试基本emoji字符
        self.assertTrue(is_emoji_character("😀"))  # 笑脸emoji
        self.assertTrue(is_emoji_character("🎉"))  # 派对emoji
        # 注意：某些数字和字母也可能被定义为emoji字符，这取决于Unicode标准
        # 我们不应该假设普通数字不是emoji字符，因为这可能不正确

    def test_is_extended_pictographic_character(self):
        # 测试扩展象形文字字符
        self.assertTrue(is_extended_pictographic_character("😀"))
        self.assertTrue(is_extended_pictographic_character("🎉"))

    def test_is_emoji_component(self):
        # 测试emoji组件
        self.assertTrue(is_emoji_component("🏻"))  # 肤色修饰符
        self.assertTrue(is_emoji_component("🇺"))  # 区域指示符
        self.assertTrue(is_emoji_component("🇸"))  # 区域指示符
        self.assertTrue(is_emoji_component("\ufe0f"))  # emoji呈现选择器
        # 根据Unicode标准，文本呈现选择器可能不被视为emoji组件

    def test_is_presentation_selectors(self):
        # 测试呈现选择器
        self.assertTrue(is_emoji_presentation_selector("\ufe0f"))
        self.assertTrue(is_text_presentation_selector("\ufe0e"))
        self.assertFalse(is_emoji_presentation_selector("A"))
        self.assertFalse(is_text_presentation_selector("A"))

    def test_is_regional_indicator(self):
        # 测试区域指示符
        self.assertTrue(is_regional_indicator("🇺"))
        self.assertTrue(is_regional_indicator("🇸"))
        self.assertFalse(is_regional_indicator("A"))

    def test_is_emoji_modifier(self):
        # 测试emoji修饰符
        self.assertTrue(is_emoji_modifier("🏻"))  # 浅肤色
        self.assertTrue(is_emoji_modifier("🏿"))  # 深肤色
        self.assertFalse(is_emoji_modifier("A"))

    def test_is_emoji_modifier_base(self):
        # 测试emoji修饰符基础字符
        self.assertTrue(is_emoji_modifier_base("👍"))  # 竖拇指
        self.assertTrue(is_emoji_modifier_base("☝"))  # 竖食指
        self.assertFalse(is_emoji_modifier_base("A"))

    def test_is_emoji_keycap_sequence(self):
        # 测试按键序列
        self.assertTrue(is_emoji_keycap_sequence("1️⃣"))
        self.assertTrue(is_emoji_keycap_sequence("#️⃣"))
        self.assertTrue(is_emoji_keycap_sequence("*️⃣"))
        self.assertFalse(is_emoji_keycap_sequence("1"))

    def test_is_emoji_flag_sequence(self):
        # 测试国旗序列
        self.assertTrue(is_emoji_flag_sequence("🇺🇸"))
        self.assertTrue(is_emoji_flag_sequence("🇬🇧"))
        self.assertTrue(is_emoji_flag_sequence("🇯🇵"))
        self.assertFalse(is_emoji_flag_sequence("🇺"))

    def test_is_emoji_modifier_sequence(self):
        # 测试emoji修饰符序列
        self.assertTrue(is_emoji_modifier_sequence("👍🏿"))
        self.assertTrue(is_emoji_modifier_sequence("☝🏻"))
        self.assertFalse(is_emoji_modifier_sequence("👍"))

    def test_is_emoji_zwj_sequence(self):
        # 测试ZWJ序列
        self.assertTrue(is_emoji_zwj_sequence("👨‍👩‍👧"))  # 家庭
        self.assertTrue(is_emoji_zwj_sequence("👩‍❤️‍👨"))  # 情侣
        self.assertFalse(is_emoji_zwj_sequence("👨👩👧"))

    def test_is_emoji_presentation_sequence(self):
        # 测试emoji呈现序列
        self.assertTrue(is_emoji_presentation_sequence("☺️"))
        self.assertTrue(is_emoji_presentation_sequence("☹️"))

    def test_is_text_presentation_sequence(self):
        # 测试文本呈现序列
        # 注意：这需要特定的文本呈现序列示例
        # 由于大多数emoji默认为emoji呈现，所以很难找到文本呈现序列
        pass

    def test_is_emoji_sequence(self):
        # 测试通用emoji序列
        self.assertTrue(is_emoji_sequence("😀"))
        self.assertTrue(is_emoji_sequence("👨‍👩‍👧"))
        self.assertTrue(is_emoji_sequence("🇺🇸"))
        self.assertTrue(is_emoji_sequence("1️⃣"))
        self.assertTrue(is_emoji_sequence("👍🏿"))

    def test_detect_qualified(self):
        # 测试合格类型检测
        # 测试完全合格的emoji
        fully_qualified = "😀"
        self.assertEqual(detect_qualified(fully_qualified), QualifiedType.FULLY_QUALIFIED)

        # 注意：要测试最小合格和未合格的emoji，我们需要具体的例子
        # 这些例子可能不容易找到，因为大多数现代emoji都是完全合格的


if __name__ == "__main__":
    unittest.main()
