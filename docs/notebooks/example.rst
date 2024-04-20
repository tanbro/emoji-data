Example
=======

Class ``EmojiSequence`` is most useful To use it:

Usages
------

Import ``emoji_data``:

.. code:: python

    from emoji_data import EmojiSequence

Print Emojis
~~~~~~~~~~~~

Print first 50 emojis

.. code:: python

    for es, _ in zip(EmojiSequence.values(), range(50)):
        print(repr(es))


.. parsed-literal::

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
    <EmojiSequence code_points='0033 FE0E' status='', string='3︎', description='text style;'>
    <EmojiSequence code_points='0033 FE0F' status='', string='3️', description='emoji style;'>
    <EmojiSequence code_points='0034 FE0E' status='', string='4︎', description='text style;'>
    <EmojiSequence code_points='0034 FE0F' status='', string='4️', description='emoji style;'>
    <EmojiSequence code_points='0035 FE0E' status='', string='5︎', description='text style;'>
    <EmojiSequence code_points='0035 FE0F' status='', string='5️', description='emoji style;'>
    <EmojiSequence code_points='0036 FE0E' status='', string='6︎', description='text style;'>
    <EmojiSequence code_points='0036 FE0F' status='', string='6️', description='emoji style;'>
    <EmojiSequence code_points='0037 FE0E' status='', string='7︎', description='text style;'>
    <EmojiSequence code_points='0037 FE0F' status='', string='7️', description='emoji style;'>
    <EmojiSequence code_points='0038 FE0E' status='', string='8︎', description='text style;'>
    <EmojiSequence code_points='0038 FE0F' status='', string='8️', description='emoji style;'>
    <EmojiSequence code_points='0039 FE0E' status='', string='9︎', description='text style;'>
    <EmojiSequence code_points='0039 FE0F' status='', string='9️', description='emoji style;'>
    <EmojiSequence code_points='00A9 FE0E' status='', string='©︎', description='text style;'>
    <EmojiSequence code_points='00A9 FE0F' status='', string='©️', description='copyright'>
    <EmojiSequence code_points='00AE FE0E' status='', string='®︎', description='text style;'>
    <EmojiSequence code_points='00AE FE0F' status='', string='®️', description='registered'>
    <EmojiSequence code_points='203C FE0E' status='', string='‼︎', description='text style;'>
    <EmojiSequence code_points='203C FE0F' status='', string='‼️', description='double exclamation mark'>
    <EmojiSequence code_points='2049 FE0E' status='', string='⁉︎', description='text style;'>
    <EmojiSequence code_points='2049 FE0F' status='', string='⁉️', description='exclamation question mark'>
    <EmojiSequence code_points='2122 FE0E' status='', string='™︎', description='text style;'>
    <EmojiSequence code_points='2122 FE0F' status='', string='™️', description='trade mark'>
    <EmojiSequence code_points='2139 FE0E' status='', string='ℹ︎', description='text style;'>
    <EmojiSequence code_points='2139 FE0F' status='', string='ℹ️', description='information'>
    <EmojiSequence code_points='2194 FE0E' status='', string='↔︎', description='text style;'>
    <EmojiSequence code_points='2194 FE0F' status='', string='↔️', description='left-right arrow'>
    <EmojiSequence code_points='2195 FE0E' status='', string='↕︎', description='text style;'>
    <EmojiSequence code_points='2195 FE0F' status='', string='↕️', description='up-down arrow'>
    <EmojiSequence code_points='2196 FE0E' status='', string='↖︎', description='text style;'>
    <EmojiSequence code_points='2196 FE0F' status='', string='↖️', description='up-left arrow'>
    <EmojiSequence code_points='2197 FE0E' status='', string='↗︎', description='text style;'>
    <EmojiSequence code_points='2197 FE0F' status='', string='↗️', description='up-right arrow'>
    <EmojiSequence code_points='2198 FE0E' status='', string='↘︎', description='text style;'>
    <EmojiSequence code_points='2198 FE0F' status='', string='↘️', description='down-right arrow'>
    <EmojiSequence code_points='2199 FE0E' status='', string='↙︎', description='text style;'>
    <EmojiSequence code_points='2199 FE0F' status='', string='↙️', description='down-left arrow'>
    <EmojiSequence code_points='21A9 FE0E' status='', string='↩︎', description='text style;'>
    <EmojiSequence code_points='21A9 FE0F' status='', string='↩️', description='right arrow curving left'>


Check if hex list represents an EmojiSequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

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
            print('{} is NOT EmojiSequence!'.format(hex_data))
        else:
            print('{} is EmojiSequence {}'.format(hex_data, es.string))


.. parsed-literal::

    1F6A3 is EmojiSequence 🚣
    1F468 1F3FC 200D F68F is NOT EmojiSequence!
    1F468 1F3FB 200D 2708 FE0F is EmojiSequence 👨🏻‍✈️
    023A is NOT EmojiSequence!
    1F469 200D 1F52C is EmojiSequence 👩‍🔬
    1F468 200D 1F468 200D 1F467 200D 1F467 is EmojiSequence 👨‍👨‍👧‍👧
    1F441 FE0F 200D 1F5E8 FE0E is NOT EmojiSequence!


Check if a string is EmojiSequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    print('👨' in EmojiSequence)
    print('©' in EmojiSequence)  # 00AE, unqualified
    print('5️⃣' in EmojiSequence)
    print('9⃣' in EmojiSequence)  # 0039 20E3, unqualified


.. parsed-literal::

    True
    False
    True
    False


Search EmojiSequence inside texts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    strings = [
        "First:👨🏻‍⚕️. Second:👨🏻.",
        "The two emojis 👨‍👨‍👧👨‍👨‍👧‍👧 are long. Today is a 🌞⛈️ day, I am 😀.",
        "© 00AE is unqualified, the full-qualified one is 00A9 FE0F ©️",
        "9⃣ 0039 20E3 is also unqualified, it will not be matched!",
        "and no more emoji."
    ]

    for s in strings:
        for es, begin, end in EmojiSequence.find(s):
            print(f'[{begin}:{end}] - {es} {es!r}')
        print('---')


.. parsed-literal::

    [6:11] - 👨🏻‍⚕️ <EmojiSequence code_points='1F468 1F3FB 200D 2695 FE0F' status='', string='👨🏻\u200d⚕️', description='man health worker: light skin tone'>
    [20:22] - 👨🏻 <EmojiSequence code_points='1F468 1F3FB' status='', string='👨🏻', description='man: light skin tone'>
    ---
    [15:20] - 👨‍👨‍👧 <EmojiSequence code_points='1F468 200D 1F468 200D 1F467' status='', string='👨\u200d👨\u200d👧', description='family: man, man, girl'>
    [20:27] - 👨‍👨‍👧‍👧 <EmojiSequence code_points='1F468 200D 1F468 200D 1F467 200D 1F467' status='', string='👨\u200d👨\u200d👧\u200d👧', description='family: man, man, girl, girl'>
    [49:50] - 🌞 <EmojiSequence code_points='1F31E' status='', string='🌞', description='full moon face..sun with face'>
    [50:52] - ⛈️ <EmojiSequence code_points='26C8 FE0F' status='', string='⛈️', description='cloud with lightning and rain'>
    [63:64] - 😀 <EmojiSequence code_points='1F600' status='', string='😀', description='grinning face'>
    ---
    [59:61] - ©️ <EmojiSequence code_points='00A9 FE0F' status='', string='©️', description='copyright'>
    ---
    ---
    ---
