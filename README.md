# emoji-data

[![CircleCI](https://circleci.com/gh/tanbro/emoji-data.svg?style=svg)](https://circleci.com/gh/tanbro/emoji-data)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c37877dfc4184233917fec36a827c47c)](https://app.codacy.com/app/tanbro/emoji-data?utm_source=github.com&utm_medium=referral&utm_content=tanbro/emoji-data&utm_campaign=Badge_Grade_Dashboard)
[![Documentation Status](https://readthedocs.org/projects/emoji-data/badge/?version=latest)](https://emoji-data.readthedocs.io/en/latest/?badge=latest)

---

A library represents [emoji][] sequences and characters from the data files listed in [Unicode][]® Technical Standard #51([UNICODE EMOJI](http://www.unicode.org/reports/tr51/>))

## How to use

Examples below also in a [notebook](notebooks/example.ipynb)

Class `EmojiSequence` is most useful:

### Iterate print Emojis

```python
from emoji_data import EmojiSequence

emojis_list = []
for _, es in EmojiSequence:
    emojis_list.append(es)

print(emojis_list)
```

Output:

    [<EmojiSequence code_points='1F468 200D 2764 FE0F 200D 1F468' status='fully-qualified', string='👨\u200d❤️\u200d👨', description='couple with heart: man, man'>,
     <EmojiSequence code_points='1F468 200D 2764 FE0F 200D 1F48B 200D 1F468' status='fully-qualified', string='👨\u200d❤️\u200d💋\u200d👨', description='kiss: man, man'>,
     <EmojiSequence code_points='1F468 200D 1F466' status='fully-qualified', string='👨\u200d👦', description='family: man, boy'>,
     <EmojiSequence code_points='1F468 200D 1F466 200D 1F466' status='fully-qualified', string='👨\u200d👦\u200d👦', description='family: man, boy, boy'>,
     <EmojiSequence code_points='1F468 200D 1F467' status='fully-qualified', string='👨\u200d👧', description='family: man, girl'>,
     ...]

### Check if hex list represents an Emoji

```python
from emoji_data import EmojiSequence

emojis_data = [
    '1F6A3',
    '1F468 1F3FC 200D F68F',
    '1F468 1F3FB 200D 2708 FE0F',
    '023A',
    '1F469 200D 1F52C',
    '1F468 200D 1F468 200D 1F467 200D 1F467',
    '1F441 FE0F 200D 1F5E8 FE0E'
]

for hex_data in emojis_data:
    try:
        es = EmojiSequence.from_hex(hex_data)
    except KeyError:
        print('{} is NOT Emoji!'.format(hex_data))
    else:
        print('{} is Emoji {}'.format(hex_data, es.string))
```

Output:

    1F6A3 is Emoji 🚣
    1F468 1F3FC 200D F68F is NOT Emoji!
    1F468 1F3FB 200D 2708 FE0F is Emoji 👨🏻‍✈️
    023A is NOT Emoji!
    1F469 200D 1F52C is Emoji 👩‍🔬
    1F468 200D 1F468 200D 1F467 200D 1F467 is Emoji 👨‍👨‍👧‍👧
    1F441 FE0F 200D 1F5E8 FE0E is NOT Emoji!

### Check if a string is Emoji

```python
from emoji_data import EmojiSequence

print('👨' in EmojiSequence)
print('©' in EmojiSequence)  # 00AE, unqualified
print('5️⃣' in EmojiSequence)
print('9⃣' in EmojiSequence)  # 0039 20E3, unqualified
```

Output:

    True
    True
    True
    True

### Search Emojis inside texts

```python
from emoji_data import EmojiSequence

pat = EmojiSequence.pattern

strings = [
    "First:👨🏻‍⚕️. Second:👨🏻.",
    "The two emojis 👨‍👨‍👧👨‍👨‍👧‍👧 are long. Today is a 🌞⛈️ day, I am 😀.",
    "© 00AE is unqualified, the full-qualified one is 00A9 FE0F ©️",
    "9⃣ 0039 20E3 is also unqualified, but it can be matched!"
]

for s in strings:
    m = pat.search(s)
    while m:
        assert m.group() in EmojiSequence
        print('[{} : {}] : {}'.format(m.start(), m.end(), m.group()))
        m = pat.search(s, m.end())
    print('------')
```

Output:

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

---

[unicode]: https://unicode.org/
[emoji]: https://unicode.org/emoji/index.html
