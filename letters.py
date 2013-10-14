from __future__ import print_function

words = [w.strip() for w in open('/usr/share/dict/words').readlines()]
words = [w for w in words if len(w) <= len('countdown')]

def letters_round(letters):
    winning_length = len(winning_word(letters))
    print(winning_length)
    for word in possible_words(letters):
        if len(word) == winning_length:
            print(word)

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
