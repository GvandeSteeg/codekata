import os
from itertools import permutations
from pprint import pprint

word_finder_list = ['C', 'R', 'C', 'E', 'I', 'N', 'E', 'C', 'T']

permutation_words = set()
for i in range(4, 10):
    permutation_words.update(permutations(word_finder_list, i))

permutation_words = {''.join(x).lower() for x in permutation_words if 'I' in x}

with open(os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'resources', 'english-words', 'words_alpha.txt'))) as f:
    dictwords = {l.strip() for l in f if len(l) >= 4 and len(l) <= 9}

result = {word for word in permutation_words if word in dictwords}

print(len(result))
print(len(dictwords))

pprint(result)