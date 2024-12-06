#!/usr/bin/env bash

set -eux

urls=(
    https://www.unicode.org/Public/16.0.0/ucd/emoji/emoji-data.txt
    https://www.unicode.org/Public/16.0.0/ucd/emoji/emoji-variation-sequences.txt
    https://www.unicode.org/Public/emoji/16.0/emoji-sequences.txt
    https://www.unicode.org/Public/emoji/16.0/emoji-zwj-sequences.txt
    https://www.unicode.org/Public/emoji/16.0/emoji-test.txt
)

for url in ${urls[@]}
do
  wget -cNP src/emoji_data/data $url
done
