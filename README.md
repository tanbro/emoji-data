# emoji-data

[![CircleCI](https://github.com/tanbro/emoji-data/actions/workflows/python-package.yml/badge.svg)](https://github.com/tanbro/emoji-data/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/emoji-data/badge/?version=latest)](https://emoji-data.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/emoji-data.svg)](https://pypi.org/project/emoji-data/)

A library represents emoji sequences and characters in [Unicode® Technical Standard #51 Data Files](http://www.unicode.org/reports/tr51/#Data_Files_Table)

## How to use

Examples below are also in a [notebook](notebooks/example)

Class `EmojiSequence` is most useful:

### Iterate Emojis

Print first 5 emoji sequence objects:

```python
>>> from emoji_data import EmojiSequence
>>> for (s, seq), *_ in zip(EmojiSequence.items(), range(5)):
>>>     print(s, repr(seq))
👨‍❤️‍👨 <EmojiSequence code_points='1F468 200D 2764 FE0F 200D 1F468' status='fully-qualified', string='👨\u200d❤️\u200d👨', description='couple with heart: man, man'>
👨‍❤️‍💋‍👨 <EmojiSequence code_points='1F468 200D 2764 FE0F 200D 1F48B 200D 1F468' status='fully-qualified', string='👨\u200d❤️\u200d💋\u200d👨', description='kiss: man, man'>
👨‍👦 <EmojiSequence code_points='1F468 200D 1F466' status='fully-qualified', string='👨\u200d👦', description='family: man, boy'>
👨‍👦‍👦 <EmojiSequence code_points='1F468 200D 1F466 200D 1F466' status='fully-qualified', string='👨\u200d👦\u200d👦', description='family: man, boy, boy'>
👨‍👧 <EmojiSequence code_points='1F468 200D 1F467' status='fully-qualified', string='👨\u200d👧', description='family: man, girl'>
```

### Convert HEX to Emoji

```python
>>> from emoji_data import EmojiSequence

>>> emojis_data = [
>>>     '1F6A3',
>>>     '1F468 1F3FC 200D F68F',
>>>     '1F468 1F3FB 200D 2708 FE0F',
>>>     '023A',
>>>     '1F469 200D 1F52C',
>>>     '1F468 200D 1F468 200D 1F467 200D 1F467',
>>>     '1F441 FE0F 200D 1F5E8 FE0E'
>>> ]

>>> for hex_data in emojis_data:
>>>     try:
>>>         es = EmojiSequence.from_hex(hex_data)
>>>     except KeyError:
>>>         print('{} is NOT Emoji!'.format(hex_data))
>>>     else:
>>>         print('{} is Emoji {}'.format(hex_data, es.string))
1F 6A3 is Emoji 🚣
1F468 1F3FC 200D F68F is NOT Emoji!
1F468 1F3FB 200D 2708 FE0F is Emoji 👨🏻‍✈️
023A is NOT Emoji!
1F469 200D 1F52C is Emoji 👩‍🔬
1F468 200D 1F468 200D 1F467 200D 1F467 is Emoji 👨‍👨‍👧‍👧
1F441 FE0F 200D 1F5E8 FE0E is NOT Emoji!
```

### Check if a string is Emoji

```python
>>> from emoji_data import EmojiSequence

>>> print('👨' in EmojiSequence)
True
>>> print('©' in EmojiSequence)  # 00AE, unqualified
True
>>> print('5️⃣' in EmojiSequence)
True
>>> print('9⃣' in EmojiSequence)  # 0039 20E3, unqualified
True
```

### Search Emojis in text

```python
>>> from emoji_data import EmojiSequence

>>> strings = [
>>>     "First:👨🏻‍⚕️. Second:👨🏻.",
>>>     "The two emojis 👨‍👨‍👧👨‍👨‍👧‍👧 are long. Today is a 🌞⛈️ day, I am 😀.",
>>>     "© 00AE is unqualified, the full-qualified one is 00A9 FE0F ©️",
>>>     "9⃣ 0039 20E3 is also unqualified, but it can be matched!"
>>> ]

>>> for s in strings:
>>>     for es, begin, end in EmojiSequence.iter_find(s):
>>>         print('[{} : {}] : {}'.format(begin, end, es))
>>>     print('------')
[6 : 11] : 👨🏻‍⚕️
[20 : 22] : 👨🏻
------
[15 : 20] : 👨‍👨‍👧
[20 : 27] : 👨‍👨‍👧‍👧
[49 : 50] : 🌞
[50 : 52] : ⛈️
[63 : 64] : 😀
------
[0 : 1] : ©
[59 : 61] : ©️
------
[0 : 2] : 9⃣
```
