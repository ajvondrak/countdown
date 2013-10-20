from __future__ import print_function
from countdown.config import *

words = [w.strip() for w in open(getDictionaryLocation()).readlines()]
words = [w for w in words if len(w) <= len('countdown')]
words = [w for w in words if w.isalpha() and w.islower()]

def letters_round(letters):
    # I would wrap this stuff in countdown.clock, but it runs so fast that it's
    # not really a concern.
    winning_length = len(winning_word(letters))
    print(winning_length)
    for word in possible_words(letters):
        if len(word) == winning_length:
            print(word)
    if winning_length == 9:
        # Double score for using all nine letters
        return 18
    return winning_length

def winning_word(letters):
    return max(possible_words(letters), key=len)

def possible_words(letters):
    for word in words:
        if could_form(word, letters):
            yield word

def could_form(word, letters):
    return uses_letters(word, letters) and enough_of_each_letter(word, letters)

def uses_letters(word, letters):
    return set(word).issubset(set(letters))

def enough_of_each_letter(word, letters):
    return all(word.count(l) <= letters.count(l) for l in set(letters))
