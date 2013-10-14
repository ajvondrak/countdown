from __future__ import print_function
from countdown.letters import words
import os.path
import pickle
import sys

def is_anagram(word1, word2):
    return ''.join(sorted(word1)) == ''.join(sorted(word2))

def anagrams(word):
    for anagram in words:
        if is_anagram(word, anagram):
            yield anagram

def teaser(clue):
    for anagram in anagrams(clue):
        print('It might be:', anagram)

def conundrum(word):
    answer = next(anagrams(word), None)
    print(answer)
    return answer

if os.path.exists('countdown/conundrums.pickle'):
    sys.stdout.write('Loading countdown/conundrums.pickle...')
    sys.stdout.flush()
    with open('countdown/conundrums.pickle', 'r') as pickle_file:
        conundrums = pickle.load(pickle_file)
    print('done.\n')
else:
    print('*** GENERATING CONUNDRUMS (this may take awhile) ***\n')

    sys.stdout.write('Pre-processing...')
    sys.stdout.flush()

    nine_letter_words = [w for w in words if len(w) == len('countdown')]
    nine_letter_sorts = [''.join(sorted(w.lower())) for w in nine_letter_words]

    words_to_sorts = dict(zip(nine_letter_words, nine_letter_sorts))
    sorts_to_words = {}

    for word, sort in words_to_sorts.iteritems():
        if nine_letter_sorts.count(sort) == 1:
            sorts_to_words[sort] = word

    print('done.')
    print('\nMain processing:')
    sys.stdout.write('Phase 1 of 5...')
    sys.stdout.flush()

    conundrums = {}

    for word1_len in range(2, 6):
        word2_len = 9 - word1_len
        words1 = [w for w in words if len(w) == word1_len]
        words2 = [w for w in words if len(w) == word2_len]
        for w1 in words1:
            for w2 in words2:
                if w1 + w2 in words_to_sorts or w2 + w1 in words_to_sorts:
                    # e.g., "spareribs" = "spare" + "ribs" is trivial
                    continue
                sort = ''.join(sorted(w1 + w2))
                if sort in sorts_to_words:
                    answer = sorts_to_words[sort]
                    conundrums[(w1, w2)] = answer
        print('done.')
        sys.stdout.write('Phase {} of 5...'.format(word1_len))
        sys.stdout.flush()

    print('done.')
    sys.stdout.write('\nSaving results to countdown/conundrums.pickle...')
    sys.stdout.flush()
    with open('countdown/conundrums.pickle', 'w') as pickle_file:
        pickle.dump(conundrums, pickle_file)
    print('done.\n')
