import itertools
import json
import re
from pprint import pprint
from typing import List


def load_values():
    with open("day1.json") as f:
        json_o = json.load(f)
        board = json_o["board"]
        letters = json_o["letters"]
        return board, letters


def get_all_words(board):
    words = []
    for row in board:
        word = " ".join(map(str, row)).split("0")
        word = [w.strip(" ") for w in word]
        words += [w.split(' ') for w in word if " " in w]

    return words


def get_word_dict():
    with open("../resources/english-words/words_alpha.txt") as f:
        words_alpha_list = {l.strip() for l in f}
    return words_alpha_list


board, letters = load_values()
words = get_all_words(board)

board_t = list(zip(*board))
words.extend(get_all_words(board_t))


def replacer(wordlist: List[str]):
    for word in wordlist:
        for i in range(len(word)):
            try:
                word[i] = letters[word[i]]
            except KeyError:
                continue
    return wordlist


print(len(words))
print(words)

words = replacer(words)
unique_letters = set(itertools.chain(*words))
x = dict()
for i in unique_letters:
    x[i] = [u for u in words if i in u]

z = list(itertools.permutations(x['4'], 2))

print(z)
