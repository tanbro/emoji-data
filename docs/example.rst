Example
=======

Class ``EmojiSequence`` is most usefule. To use it:

Usages
------

Import ``emoji_data``:

.. code:: ipython3

    from emoji_data import EmojiSequence

Print Emojis
~~~~~~~~~~~~

Print 10 emojis

.. code:: ipython3

    for i, es in enumerate(EmojiSequence.values()):
        if i < 10:
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
    

Check if hex list represents an EmojiSequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

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

.. code:: ipython3

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

.. code:: ipython3

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
    [50:52] - ⛈️ <EmojiSequence code_points='26C8 FE0F' status='', string='⛈️', description='emoji style;'>
    [63:64] - 😀 <EmojiSequence code_points='1F600' status='', string='😀', description='grinning face'>
    ---
    [59:61] - ©️ <EmojiSequence code_points='00A9 FE0F' status='', string='©️', description='emoji style;'>
    ---
    ---
    ---
    
