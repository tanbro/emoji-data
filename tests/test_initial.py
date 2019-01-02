# -*- coding: utf-8 -*-

from unittest import TestCase

from emoji_data import EMOJI_DATA_URL, EmojiData


class InitialTest(TestCase):

    def test_data(self):
        EmojiData.initial()
        self.assertGreater(len(EmojiData), 0)

    def test_url(self):
        EmojiData.initial(EMOJI_DATA_URL)
        self.assertGreater(len(EmojiData), 0)

    def test_file(self):
        EmojiData.initial('src/emoji_data/data/emoji-data.txt')
        self.assertGreater(len(EmojiData), 0)
