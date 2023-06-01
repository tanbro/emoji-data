# emoji-data

[![CircleCI](https://github.com/tanbro/emoji-data/actions/workflows/python-package.yml/badge.svg)](https://github.com/tanbro/emoji-data/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/emoji-data/badge/?version=latest)](https://emoji-data.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/emoji-data.svg)](https://pypi.org/project/emoji-data/)

A library represents emoji sequences and characters in [Unicode® Technical Standard #51 Data Files](http://www.unicode.org/reports/tr51/#Data_Files_Table)

## Install

```sh
pip install emoji-data
```

## How to use

Examples below are also in a [notebook](notebooks/example.ipynb)

Class `EmojiSequence` is most usefule. To use it:

Import `emoji_data`:

```python
from emoji_data import EmojiSequence
```

### Print Emojis

Print 10 emojis

```python
>>> for i, es in enumerate(EmojiSequence.values()):
>>>     if i < 10:
>>>         print(repr(es))
    <EmojiSequence code_points='0023 FE0E' status='', string='#︎', description='text style;'>
    <EmojiSequence code_points='0023 FE0F' status='', string='#️', description='emoji style;'>
    <EmojiSequence code_points='002A FE0E' status='', string='*︎', description='text style;'>
    <EmojiSequence code_points='002A FE0F' status='', string='*️', description='emoji style;'>
    <EmojiSequence code_points='0030 FE0E' status='', string='0︎', description='text style;'>
    <EmojiSequence code_points='0030 FE0F' status='', string='0️', description='emoji style;'>
    <EmojiSequence code_points='0031 FE0E' status='', string='1︎', description='text style;'>
    <EmojiSequence code_points='0031 FE0F' status='', string='1️', description='emoji style;'>
    <EmojiSequence code_points='0032 FE0E' status='', string='2︎', description='text style;'>
    <EmojiSequence code_points='0032 FE0F' status='', string='2️', description='emoji style;'>
```

### Check if hex list represents an EmojiSequence

```python
>>> emojis_data = [
        '1F6A3',
        '1F468 1F3FC 200D F68F',
        '1F468 1F3FB 200D 2708 FE0F',
        '023A',
        '1F469 200D 1F52C',
        '1F468 200D 1F468 200D 1F467 200D 1F467',
        '1F441 FE0F 200D 1F5E8 FE0E'
    ]

>>> for hex_data in emojis_data:
>>>     try:
>>>         es = EmojiSequence.from_hex(hex_data)
>>>     except KeyError:
>>>         print('{} is NOT EmojiSequence!'.format(hex_data))
>>>     else:
>>>         print('{} is EmojiSequence {}'.format(hex_data, es.string))
    1F6A3 is EmojiSequence 🚣
    1F468 1F3FC 200D F68F is NOT EmojiSequence!
    1F468 1F3FB 200D 2708 FE0F is EmojiSequence 👨🏻‍✈️
    023A is NOT EmojiSequence!
    1F469 200D 1F52C is EmojiSequence 👩‍🔬
    1F468 200D 1F468 200D 1F467 200D 1F467 is EmojiSequence 👨‍👨‍👧‍👧
    1F441 FE0F 200D 1F5E8 FE0E is NOT EmojiSequence!
```

### Check if a string is EmojiSequence

```python
>>> print('👨' in EmojiSequence)
    True
>>> print('©' in EmojiSequence)  # 00AE, unqualified
    False
>>> print('5️⃣' in EmojiSequence)
    True
>>> print('9⃣' in EmojiSequence)  # 0039 20E3, unqualified
    False
```

### Search EmojiSequence inside texts

```python
>>> strings = [
        "First:👨🏻‍⚕️. Second:👨🏻.",
        "The two emojis 👨‍👨‍👧👨‍👨‍👧‍👧 are long. Today is a 🌞⛈️ day, I am 😀.",
        "© 00AE is unqualified, the full-qualified one is 00A9 FE0F ©️",
        "9⃣ 0039 20E3 is also unqualified, it will not be matched!",
        "and no more emoji."
    ]
>>>
>>> for s in strings:
>>>     for es, begin, end in EmojiSequence.find(s):
>>>         print(f'[{begin}:{end}] - {es} {es!r}')
>>>     print('---')
    [6:11] - 👨🏻‍⚕️ <EmojiSequence code_points='1F468 1F3FB 200D 2695 FE0F' status='', string='👨🏻\u200d⚕️', description='man health worker: light skin tone'>
    [20:22] - 👨🏻 <EmojiSequence code_points='1F468 1F3FB' status='', string='👨🏻', description='man: light skin tone'>
    ---
    [15:20] - 👨‍👨‍👧 <EmojiSequence code_points='1F468 200D 1F468 200D 1F467' status='', string='👨\u200d👨\u200d👧', description='family: man, man, girl'>
    [20:27] - 👨‍👨‍👧‍👧 <EmojiSequence code_points='1F468 200D 1F468 200D 1F467 200D 1F467' status='', string='👨\u200d👨\u200d👧\u200d👧', description='family: man, man, girl, girl'>
    [49:50] - 🌞 <EmojiSequence code_points='1F31E' status='', string='🌞', description='full moon face..sun with face'>
    [50:52] - ⛈️ <EmojiSequence code_points='26C8 FE0F' status='', string='⛈️', description='emoji style;'>
    [63:64] - 😀 <EmojiSequence code_points='1F600' status='', string='😀', description='grinning face'>
    ---
    [59:61] - ©️ <EmojiSequence code_points='00A9 FE0F' status='', string='©️', description='emoji style;'>
    ---
    ---
    ---
```
