from __future__ import print_function

def anagrams(word):
    for anagram in words:
        if ''.join(sorted(word)) == ''.join(sorted(anagram)):
            yield anagram

def teaser(clue):
    for anagram in anagrams(clue):
        print('It might be:', anagram)

def conundrum(word):
    print(next(anagrams(word)))
