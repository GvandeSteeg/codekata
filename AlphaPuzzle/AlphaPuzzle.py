import itertools
import json
import os
import pdb
import re
from collections import defaultdict
from copy import deepcopy
from pprint import pprint
from string import ascii_letters, ascii_uppercase
from time import sleep
from typing import List, Union, Tuple, Dict, Set, Sequence

with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'english-words', 'words_alpha.txt')) as f:
    alpha_words = {line.strip().upper() for line in f}

num_range = set(map(str, range(1, len(ascii_uppercase) + 1)))


def load_values() -> Tuple[List[List[str]], Dict[str, List[List[str]]]]:
    with open("day1.json") as f:
        json_o = json.load(f)
        board = json_o["board"]
        letters = json_o["letters"]
        return board, letters


def get_all_words(board: Sequence[Sequence[str]]) -> List[str]:
    all_words = []
    for row in board:
        wo = "-".join(map(str, row)).split('-0-')
        word = [w.strip("-") for w in wo]
        words = [w.split('-') for w in word if "-" in w]
        for w in words:
            try:
                w.remove('0')
            except ValueError:
                pass

        all_words += words

    return all_words


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


def generate_crosslinks(words: Sequence[Sequence[str]]):
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

    return my_set


def potential_words(word: Sequence[str], alphawords: Set[str]):
    """
    Finds words that could match a given cypher

    A potential word must match the following requirements
    - Length equal to length word
    - Each known character in word must match on the same location
    - If an integer in word appears in multiple locations, potential word must have the same letter in both locations

    :param word: Tuple of string representation of integers, unless a character is already known
    """

    # Hash word
    word_hash = defaultdict(list)
    for i, j in enumerate(word):
        word_hash[j].append(i)

    potential_words = set()
    for potential_word in alphawords:
        fail = False

        # Compare length of words
        if len(potential_word) != len(word):
            continue

        # If any known letters are not in potential word, skip
        for k in (u for u in word_hash.keys() if u in ascii_letters):
            if k not in potential_word:
                fail = True
                break
        if fail:
            continue

        # Check whether both words have letters in the same positions
        potential_word_hash = defaultdict(list)
        for i, j in enumerate(potential_word):
            potential_word_hash[j].append(i)

        if list(word_hash.values()) != list(potential_word_hash.values()):
            continue

        # Compare known characters in both words
        for pos in range(len(word)):
            if word[pos] not in num_range:
                if word[pos] != potential_word[pos]:
                    fail = True
                    break

        if fail:
            continue

        potential_words.add(potential_word)

    return potential_words


def update_letters(cypher: Sequence[str], crack: str):
    global letters
    for i, j in zip(cypher, crack):
        letters[i] = j
    for key in deepcopy(letters):
        if key in ascii_uppercase:
            del letters[key]


def hamming_distance(word1, word2):
    if len(word1) != len(word2):
        raise ValueError(f'Lenght of both words varies! {word1}: {len(word1)}, {word2}: {len(word2)}')
    hamm = 0
    for i, j in zip(word1, word2):
        if i != j:
            hamm += 1
    return hamm


# While any numbers persist in all words
def run():
    global words
    old_len_letters = 0
    while any({i not in ascii_letters for i in ''.join((''.join(w) for w in words))}):
        words = replacer(words)
        for x in words:
            if all({i in ascii_letters for i in x}):
                # print(''.join(x))
                continue

            new_words = list(potential_words(x, alpha_words))
            if len(new_words) == 1:
                new_word = new_words[0]
                update_letters(x, new_word)

        # If no new progress is being made, interrupt while loop
        if len(letters) == old_len_letters:
            break
        else:
            # print('#' * 15)
            old_len_letters = len(letters)


def final():
    missing_keys = num_range - set(letters.keys())
    if missing_keys:
        if len(missing_keys) == 1:
            letters[list(missing_keys)[0]] = list(set(ascii_uppercase) - set(letters.values()))[0]
            run()
            final()
    else:
        print(f'Missing keys: {", ".join(missing_keys)}')
        for k in missing_keys:
            for w in words:
                if k in w:
                    print(w)


board, letters = load_values()
words = get_all_words(board)
board_t = list(zip(*board))
words.extend(get_all_words(board_t))
words = replacer(words)
run()
final()

# Print current cypher and length
pprint(sorted(letters.items(), key=lambda kv: kv[1]))
print(len(letters))
pprint(sorted(letters.items(), key=lambda kv: int(kv[0])))
pprint(list(map(lambda x: ''.join(x), words)))
