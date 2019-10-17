

import sys

current_word = None
word_count = 0

for line in sys.stdin:
    word, count = line.split("\t", 1)
    counts = int(count)
    if word == current_word:
        word_count += counts
    else:
        if current_word:
            print(current_word, word_count, sep="\t")
        current_word = word
        word_count = counts
if current_word:
    print(current_word, word_count, sep="\t")
