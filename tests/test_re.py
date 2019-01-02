# -*- coding: utf-8 -*-

from unittest import TestCase
from warnings import warn

import six

from emoji_data import EmojiData


class InitialTest(TestCase):

    def setUp(self):
        EmojiData.initial()
        self.pat = EmojiData.get_regex_pattern()
        self.assertIsNotNone(self.pat)

    def test_sub_replace(self):
        if six.PY2:
            warn("i cannot make it work on py2")
        else:
            txt = self.pat.sub('3', '12☺45')
            self.assertEqual(txt, '12345')
