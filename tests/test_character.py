import unittest

from emoji_data import EmojiCharacter, EmojiCharProperty, code_points_to_string, emoji_data_lines
from emoji_data.definitions import (
    initial_emoji_patterns,
    is_default_emoji_presentation_character,
    is_default_text_presentation_character,
    is_emoji_character,
    is_emoji_component,
    is_extended_pictographic_character,
)


class CharacterTestCase(unittest.TestCase):
    test_data = []  # type:ignore[var-annotated]

    @classmethod
    def setUpClass(cls):
        EmojiCharacter.initial()
        for content, _ in emoji_data_lines("emoji-test.txt"):
            cls.test_data.append([s.strip() for s in content.split(";", 1)])

    def test_code_points(self):
        for code_points, _ in self.test_data:
            s = code_points_to_string(code_points)
            self.assertTrue(all(ord(c) in EmojiCharacter for c in s))


class CharacterPropertyDefinitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        EmojiCharacter.initial()
        initial_emoji_patterns()

    def test_property_definition(self):
        for c in EmojiCharacter.values():
            self.assertTrue(is_emoji_character(c.string), f"{c=}")
            if EmojiCharProperty.EXTPICT in c.properties:
                self.assertTrue(is_extended_pictographic_character(c.string), f"{c=}")
            if EmojiCharProperty.ECOMP in c.properties:
                self.assertTrue(is_emoji_component(c.string), f"{c=}")
            if EmojiCharProperty.EPRES in c.properties:
                self.assertTrue(is_default_emoji_presentation_character(c.string), f"{c=}")
            if EmojiCharProperty.EPRES not in c.properties:
                self.assertTrue(is_default_text_presentation_character(c.string), f"{c=}")


if __name__ == "__main__":
    unittest.main()
