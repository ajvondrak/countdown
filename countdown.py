"""
Python does Countdown.

Quoth https://en.wikipedia.org/wiki/Countdown_%28game_show%29

    Countdown is a British game show involving word and number puzzles.

    The two contestants in each episode compete in three disciplines: eleven
    letters rounds, in which the contestants attempt to make the longest word
    possible from nine randomly chosen letters; three numbers rounds, in which
    the contestants must use arithmetic to reach a random target number from
    six other numbers; and the conundrum, a buzzer round in which the
    contestants compete to solve a nine-letter anagram.

I was watching the show and decided that it'd be easy for a computer to win it.
"""

from __future__ import print_function
from collections import deque
import random
import signal
import timeit

__all__ = ['letters_round', 'numbers_round', 'teaser', 'conundrum']

words = [w.strip() for w in open('/usr/share/dict/words').readlines()]
words = [w for w in words if len(w) <= len('countdown')]

operators = ('+', '*', '-', '/')

#####################
### Letters Round ###
#####################

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

#####################
### Numbers Round ###
#####################

def numbers_round(numbers, target):
    formulate = 'print(%s(map(str, {}), {}))'.format(numbers, target)
    import_ = 'from __main__ import backtrack_formulate, bfs_formulate'
    backtrack = timeit.Timer(formulate % 'backtrack_formulate', import_)
    bfs = timeit.Timer(formulate % 'bfs_formulate', import_)
    print('\nTime (backtrack):', backtrack.timeit(number=1), 'seconds\n')
    print('\nTime (bfs):      ', bfs.timeit(number=1), 'seconds\n')

class TimeIsUp(Exception):
    pass

def time_is_up(signum, frame):
    raise TimeIsUp()

def countdown():
    """Start a 30 second countdown to when the TimeIsUp exception is thrown."""
    signal.signal(signal.SIGALRM, time_is_up)
    signal.alarm(30)

def reset_countdown():
    signal.alarm(0)

class BestSoFar:
    def __init__(self):
        self.value = '0'

def backtrack_formulate(formulae, target):
    best_so_far = BestSoFar()
    def backtrack(formulae):
        closest = closest_to(target, formulae)
        if eval(closest) == target:
            return closest
        # need to set a reference here, because just `best_so_far` would be
        # treated like a local variable
        best_so_far.value = closest_to(target, (best_so_far.value, closest))
        for new_formulae in possible_formulae(formulae):
            answer = backtrack(new_formulae)
            if answer:
                return answer
    countdown()
    try:
        return backtrack(formulae)
    except TimeIsUp:
        print('Could only find', eval(best_so_far.value))
        return best_so_far.value
    finally:
        reset_countdown()

def bfs_formulate(formulae, target):
    best_so_far = '0'
    formulae = tuple(formulae)
    visited = set([formulae])
    worklist = deque([formulae])
    countdown()
    try:
        while worklist:
            new_formulae = worklist.popleft()
            closest = closest_to(target, new_formulae)
            if eval(closest) == target:
                return closest
            best_so_far = closest_to(target, (best_so_far, closest))
            for newer_formulae in possible_formulae(new_formulae):
                if newer_formulae not in visited:
                    visited.add(newer_formulae)
                    worklist.append(newer_formulae)
    except TimeIsUp:
        print('Could only find', eval(best_so_far))
        return best_so_far
    finally:
        reset_countdown()

def closest_to(target, formulae):
    return min(formulae, key=distance_to(target))

def distance_to(target):
    return lambda formula: abs(target - eval(formula))

def possible_formulae(formulae):
    for i1, f1 in enumerate(formulae):
        for i2, f2 in enumerate(formulae):
            if i1 == i2:
                continue
            for op in operators:
                if op == '+' and (i1 > i2 or eval(f1) == 0 or eval(f2) == 0):
                    continue
                if op == '-' and eval(f2) == 0:
                    continue
                if op == '*' and (i1 > i2 or eval(f1) == 1 or eval(f2) == 1):
                    continue
                if op == '/' and (eval(f2) == 1 or not divisible(f1, f2)):
                    continue
                yield combine(op, formulae, i1, i2)

def combine(op, formulae, index1, index2):
    combined = [f for i, f in enumerate(formulae) if i not in (index1, index2)]
    combined.append('(%s %s %s)' % (formulae[index1], op, formulae[index2]))
    return tuple(combined)

def divisible(numerator_str, denominator_str):
    numerator, denominator = eval(numerator_str), eval(denominator_str)
    return denominator != 0 and numerator % denominator == 0

##########################
### Teaser & Conundrum ###
##########################

def anagrams(word):
    for anagram in words:
        if ''.join(sorted(word)) == ''.join(sorted(anagram)):
            yield anagram

def teaser(clue):
    for anagram in anagrams(clue):
        print('It might be:', anagram)

def conundrum(word):
    print(next(anagrams(word)))

##########################
### Play the game      ###
##########################

def print_row(textwidth, cells):
    cell = '{:^3}'
    border = '+-----' * len(cells) + '+'
    row = '| ' + ' | '.join([cell] * len(cells)) + ' |'
    print(border.center(textwidth))
    print(row.format(*cells).center(textwidth))
    print(border.center(textwidth))
    print()


def play_numbers_round():
    large_numbers = [25, 50, 75, 100]
    small_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2
    # numbers = random.sample(large_numbers + small_numbers, 6)
    numbers = [9, 1, 6, 4, 4, 25]
    # target = random.randint(1, 999)
    target = 773
    print_row(40, [target])
    print_row(40, numbers)
    numbers_round(numbers, target)


if __name__ == '__main__':
    play_numbers_round()
