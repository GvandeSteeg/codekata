import json
import os
from collections import defaultdict
from pprint import pprint
from string import ascii_letters, ascii_uppercase
from typing import Dict, List, Sequence, Set, Tuple

with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'english-words', 'words_alpha.txt')) as f:
    alpha_words = {line.strip().upper() for line in f}

num_range = set(map(str, range(1, len(ascii_uppercase) + 1)))


def load_values() -> Tuple[List[List[str]], Dict[str, List[List[str]]]]:
    """Load Board and Letters from JSON"""
    with open("day1.json") as f:
        json_o = json.load(f)
        board = json_o["board"]
        letters = json_o["letters"]
        return board, letters


def get_all_words(board: Sequence[Sequence[str]]) -> List[str]:
    """Returns all words from each horizontal row in the board, splitting by 0"""
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
    """Returns a set of all alphanumeric words"""
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


# TODO Remove as crosslinks are not used?
# def generate_crosslinks(words: Sequence[Sequence[str]]):
#     unique_letters = set(itertools.chain(*words))
#     dict_of_things = dict()
#     for i in unique_letters:
#         dict_of_things[i] = [u for u in words if i in u]
#
#     my_set = set()
#     for x in dict_of_things.values():
#         x = set(map(tuple, x))
#         a = itertools.permutations(x, 2)
#         for i in a:
#             my_set.add(tuple(sorted(i)))
#
#     return my_set


def potential_words(word: Sequence[str], alphawords: Set[str]):
    """
    Finds words that could match a given cypher

    A potential word must match the following requirements
    - Length equal to length word
    - Each known character in word must match on the same location
    - If an integer in word appears in multiple locations, potential word must have the same letter in both locations

    :param word: Tuple of string representation of integers, unless a character is already known
    :param alphawords: Set of all alphanumeric words
    """

    # Hash word
    word_hash = defaultdict(list)
    for i, j in enumerate(word):
        word_hash[j].append(i)

    potential_words = set()
    for potential_word in alphawords:

        # Compare length of words
        if len(potential_word) != len(word):
            continue

        # If any known letters are not in potential word, skip
        if not all_knowns_in_potential(word_hash, potential_word):
            continue

        # Check whether both words have letters in the same positions
        if not compare_hash(word_hash, potential_word):
            continue

        # Compare known characters in both words
        if not compare_known_positions(word, potential_word):
            continue

        potential_words.add(potential_word)

    return potential_words


def compare_known_positions(word, potential_word) -> bool:
    """Returns True if every known letter in word is in exactly the same position in potential_word"""
    for pos in range(len(word)):
        if word[pos] not in num_range:
            if word[pos] != potential_word[pos]:
                return False
    return True


def compare_hash(word_hash: Dict[int, Sequence[str]], potential_word: str) -> bool:
    """
    Returns True if potential_word has duplicate values in the same positions as word

    Example:
        "APPLE" has P in pos 1 and 2;
        ["1", "2", "2", "3", "4"] has "2" in pos 1 and 2;
        Returns True

    :param word_hash: Hash of values and their positions
    :param potential_word: Alphanumeric word
    """
    potential_word_hash = defaultdict(list)
    for i, j in enumerate(potential_word):
        potential_word_hash[j].append(i)

    return list(word_hash.values()) == list(potential_word_hash.values())


def all_knowns_in_potential(word, potential_word) -> bool:
    """Returns True if potential_word contains all known characters in word"""
    for k in set(word):
        if k in ascii_letters:
            if k not in potential_word:
                return False
    return True


def update_letters(cypher: Sequence[str], crack: str) -> None:
    """
    Update global letters with new known values

    :param cypher: Word from board
    :param crack: Single alphanumeric solution to cypher
    """
    global letters
    for i, j in zip(cypher, crack):
        if i not in ascii_letters:
            letters[i] = j


# TODO remove as no longer used?
# def hamming_distance(word1, word2):
#     """Calculates the difference between two words"""
#     if len(word1) != len(word2):
#         raise ValueError(f'Lenght of both words varies! {word1}: {len(word1)}, {word2}: {len(word2)}')
#
#     hamm = 0
#     for i, j in zip(word1, word2):
#         if i != j:
#             hamm += 1
#     return hamm


# While any numbers persist in all words
def run():
    global words
    old_len_letters = 0
    while any({i not in ascii_letters for i in ''.join((''.join(w) for w in words))}):
        words = replacer(words)
        for x in words:
            if all({i in ascii_letters for i in x}):
                continue

            new_words = list(potential_words(x, alpha_words))
            if len(new_words) == 1:
                new_word = new_words[0]
                update_letters(x, new_word)

        # If no new progress is being made, interrupt while loop
        if len(letters) == old_len_letters:
            break
        else:
            old_len_letters = len(letters)


def final():
    """Check for missing keys, if 1 value persists, fill letters and rerun"""
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
pprint(sorted(letters.items(), key=lambda kv: int(kv[0])))
pprint(list(map(lambda x: ''.join(x), words)))
