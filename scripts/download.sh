#!/usr/bin/env bash

set -e

dest="src/emoji_data/data"

wget -P $dest https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-data.txt
wget -P $dest https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-variation-sequences.txt
wget -P $dest https://www.unicode.org/Public/emoji/latest/emoji-sequences.txt
wget -P $dest https://www.unicode.org/Public/emoji/latest/emoji-zwj-sequences.txt
wget -P $dest https://www.unicode.org/Public/emoji/latest/emoji-test.txt
