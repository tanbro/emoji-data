#!/usr/bin/env bash

set -eux

urls=(
    https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-data.txt
    https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-variation-sequences.txt
    https://www.unicode.org/Public/emoji/latest/emoji-sequences.txt
    https://www.unicode.org/Public/emoji/latest/emoji-zwj-sequences.txt
    https://www.unicode.org/Public/emoji/latest/emoji-test.txt
)

for url in ${urls[@]}
do
  wget -cNP src/emoji_data/data $url
done
