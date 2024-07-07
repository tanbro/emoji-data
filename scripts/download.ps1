$dest = "src/emoji_data/data"

Start-BitsTransfer -Destination $dest -Source https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-data.txt
Start-BitsTransfer -Destination $dest -Source https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-variation-sequences.txt
Start-BitsTransfer -Destination $dest -Source https://www.unicode.org/Public/emoji/latest/emoji-sequences.txt
Start-BitsTransfer -Destination $dest -Source https://www.unicode.org/Public/emoji/latest/emoji-zwj-sequences.txt
Start-BitsTransfer -Destination $dest -Source https://www.unicode.org/Public/emoji/latest/emoji-test.txt
