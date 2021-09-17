# CHANGELOG

## 0.2 (developing)

- Changes:
  - Iterator of `EmojiCharacter` and `EmojiSequence` now return only keys, no more key-value pairs

- Add:
  - `release` method for `EmojiCharacter` and `EmojiSequence`
  - `values()` and `items()` method for `EmojiCharacter` and `EmojiSequence`

## 0.1.6

- Date: 2020-01-10

- Add
  - `EmojiSequence.__len__`

- Misc
  - remove invalid value for classifiers

## 0.1.5

- Change:
  - Rename module `defines` to `definitions`

- Misc
  - Replace Codacy with CodeClimate
  - Fix Circle CI deployment problem

- Unit test:
  - Drop `pytest`, now use `unittest` in stdlib

## 0.1.4

- New
  - Load emojis from `emoji-test.txt`
  - Include `emoji-variations-sequences.txt`
  - `defines` module: many regular expresses according to <http://www.unicode.org/reports/tr51/#Definitions>

- Change
  - Many renamings
  - Some modifications of test-case

## 0.1.3

- Date: 2019-01-12

- New
  - Importing Emoji Sequence data and new `EmojiSequence` class

- Change:
  - Re-structure the project
  - Rename `EmojiData` class to `EmojiCharacter`
  - Many other changes

- Upgrade:
  - Update emoji data files to 12.0

## 0.1.2

- Date: 2019-01-10

- New
  - Sphinx documentations

## 0.1.1

- Date: 2019-01-02

- Fix bugs.
- Add Circle-CI config

## 0.1.0

- Date: 2018-12-20

First version.
