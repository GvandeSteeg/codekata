import itertools
import json
import re
from pprint import pprint
from typing import List, Union, Tuple, Dict, Set, Sequence


def load_values() -> Tuple[List[List[str]], Dict[str, List[List[str]]]]:
    with open("day1.json") as f:
        json_o = json.load(f)
        board = json_o["board"]
        letters = json_o["letters"]
        return board, letters


def get_all_words(board: Sequence[Sequence[str]]) -> List[str]:
    words = []
    for row in board:
        word = " ".join(map(str, row)).split("0")
        word = [w.strip(" ") for w in word]
        words += [w.split(' ') for w in word if " " in w]

    return words


def get_word_dict() -> Set[str]:
    with open("../resources/english-words/words_alpha.txt") as f:
        words_alpha_list = {l.strip() for l in f}
    return words_alpha_list


def replacer(wordlist: Sequence[Sequence[str]]):
    """
    For each known in the cypher, replace each integer in the wordlist with the actual letter

    Words are lists of strings
    """
    for word in wordlist:
        for i in range(len(word)):
            try:
                word[i] = letters[word[i]]
            except KeyError:
                continue
    return wordlist


board, letters = load_values()
words = get_all_words(board)

board_t = list(zip(*board))
words.extend(get_all_words(board_t))

words = replacer(words)
unique_letters = set(itertools.chain(*words))
dict_of_things = dict()
for i in unique_letters:
    dict_of_things[i] = [u for u in words if i in u]

my_set = set()
for x in dict_of_things.values():
    x = set(map(tuple, x))
    a = itertools.permutations(x, 2)
    for i in a:
        my_set.add(tuple(sorted(i)))

pprint(sorted(my_set)[:50])
print(len(my_set))

# pprint(z)
