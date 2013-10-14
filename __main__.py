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

# TODO
# clean up use of eval - class Expression: ... (which best_so_far can be, too)
# refactor signal stuff
# see about signal-ing the letters stuff, even though it shouldn't be an issue
# simulation flesh-out: point system?  human input vs playing against itself?
#   don't want to sink too much time into it...

from __future__ import print_function
from countdown.letters import *
from countdown.numbers import *
from countdown.conundrum import *
import random


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
