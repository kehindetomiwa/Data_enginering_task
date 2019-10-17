import sys
import re
from collections import Counter


'''
A simple mapper application (with combiner)

'''

for line in sys.stdin:
    flag_bg = line.startswith('BG:')

    words = re.sub(r"[^A-Za-z]", " ", line.strip())
    words = words.split()
    content = words[1:]
    counts = Counter(content)
    words_length = len(words)

    # print(words)
    if flag_bg and words_length > 1:
        for word,word_count in counts.items():
            print(word, word_count, sep="\t")
