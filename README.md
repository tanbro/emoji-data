# emoji-data

[![CircleCI](https://circleci.com/gh/tanbro/emoji-data.svg?style=svg)](https://circleci.com/gh/tanbro/emoji-data)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c37877dfc4184233917fec36a827c47c)](https://app.codacy.com/app/tanbro/emoji-data?utm_source=github.com&utm_medium=referral&utm_content=tanbro/emoji-data&utm_campaign=Badge_Grade_Dashboard)
[![Documentation Status](https://readthedocs.org/projects/emoji-data/badge/?version=latest)](https://emoji-data.readthedocs.io/en/latest/?badge=latest)

---

A library represents [emoji][] sequences and characters from the data files listed in [Unicode][]® Technical Standard #51([UNICODE EMOJI](http://www.unicode.org/reports/tr51/>))

## How to use

Examples below also in a [notebook](notebooks/example.ipynb)

Class `EmojiSequence` is most useful:

```python
from emoji_data import EmojiSequence

EmojiSequence.initial()
```

`initial()` **MUST** be called - it loads emoji data files into the class' meta data

### Iterate print Emojis

```python
>>> for s, es in EmojiSequence:
>>>    print(' '.join('{:02X}'.format(n) for n in es.codes), s)

231A ⌚
231B ⌛
23E9 ⏩
23EA ⏪
23EB ⏫
23EC ⏬
23F0 ⏰
23F3 ⏳
# ...
1F469 1F3FE 200D 1F33E 👩🏾‍🌾
1F469 1F3FE 200D 1F373 👩🏾‍🍳
1F469 1F3FE 200D 1F393 👩🏾‍🎓
1F469 1F3FE 200D 1F3A4 👩🏾‍🎤
1F469 1F3FE 200D 1F3A8 👩🏾‍🎨
1F469 1F3FE 200D 1F3EB 👩🏾‍🏫
1F469 1F3FE 200D 1F3ED 👩🏾‍🏭
1F469 1F3FE 200D 1F4BB 👩🏾‍💻
1F469 1F3FE 200D 1F4BC 👩🏾‍💼
1F469 1F3FE 200D 1F527 👩🏾‍🔧
1F469 1F3FE 200D 1F52C 👩🏾‍🔬
1F469 1F3FE 200D 1F680 👩🏾‍🚀
1F469 1F3FE 200D 1F692 👩🏾‍🚒
# ...
```

### Check if hex list represents an Emoji

```python
>>> hexes_list = [
        '1F6A3',
        '1F468 1F3FC 200D F68F',
        '1F468 1F3FB 200D 2708 FE0F',
        '023A',
        '1F469 200D 1F52C',
        '1F468 200D 1F468 200D 1F467 200D 1F467',
        '1F441 FE0F 200D 1F5E8 FE0E'
    ]

>>> for hexes in hexes_list:
>>>     try:
>>>         es = EmojiSequence.from_hexes(hexes.split())
>>>     except KeyError:
>>>         print('{} is NOT Emoji!'.format(hexes))
>>>     else:
>>>         print('{} is Emoji {}'.format(hexes, es.string))

1F6A3 is Emoji 🚣
1F468 1F3FC 200D F68F is NOT Emoji!
1F468 1F3FB 200D 2708 FE0F is Emoji 👨🏻‍✈️
023A is NOT Emoji!
1F469 200D 1F52C is Emoji 👩‍🔬
1F468 200D 1F468 200D 1F467 200D 1F467 is Emoji 👨‍👨‍👧‍👧
1F441 FE0F 200D 1F5E8 FE0E is NOT Emoji!
```

### Check if a string is Emoji

```python
>>> print('👨' in EmojiSequence)
>>> print('©' in EmojiSequence) # 00AE, unqualified
>>> print('5️⃣' in EmojiSequence)
>>> print('9⃣' in EmojiSequence)  # 0039 20E3, unqualified

True
False
True
False
```

### Search Emojis inside texts

```python
>>> pat = EmojiSequence.pattern

>>> strings = [
        "First:👨🏻‍⚕️. Second:👨🏻.",
        "I love 👨‍👨‍👧‍👧. It's ⛈️. I am 😀."
    ]

>>> for s in strings:
>>>     m = pat.search(s)
>>>     while m:
>>>         print('matched: [{} : {}] : {}'.format(m.start(), m.end(), m.group()))
>>>         m = pat.search(s, m.end())
>>>     print()

matched: [6 : 11] : 👨🏻‍⚕️
matched: [20 : 22] : 👨🏻

matched: [7 : 14] : 👨‍👨‍👧‍👧
matched: [21 : 23] : ⛈️
matched: [30 : 31] : 😀
```

---

[unicode]: https://unicode.org/
[emoji]: https://unicode.org/emoji/index.html
