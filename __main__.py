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
from countdown.letters import *
from countdown.numbers import *
from countdown.conundrum import *
import countdown.clock as clock
import random

# These 'piles' have characters repeated according to the frequency
# distribution linked on Wikipedia: http://www.thecountdownpage.com/letters.htm

vowels_pile = 'a' * 15 \
            + 'e' * 21 \
            + 'i' * 13 \
            + 'o' * 13 \
            + 'u' * 5

consonants_pile = 'b' * 2 \
                + 'c' * 3 \
                + 'd' * 6 \
                + 'f' * 2 \
                + 'g' * 3 \
                + 'h' * 2 \
                + 'j' * 1 \
                + 'k' * 1 \
                + 'l' * 5 \
                + 'm' * 4 \
                + 'n' * 8 \
                + 'p' * 4 \
                + 'q' * 1 \
                + 'r' * 9 \
                + 's' * 9 \
                + 't' * 9 \
                + 'v' * 1 \
                + 'w' * 1 \
                + 'x' * 1 \
                + 'y' * 1 \
                + 'z' * 1


def print_row(cells):
    textwidth = 80
    cell = '{:^3}'
    border = '+-----' * len(cells) + '+'
    row = '| ' + ' | '.join([cell] * len(cells)) + ' |'
    print(border.center(textwidth))
    print(row.format(*cells).center(textwidth))
    print(border.center(textwidth))
    print()


def play_letters_round():
    # The rules require at least 3 vowels and 4 consonants.  The remaining 2
    # letters are thus randomly distributed between either: 2 vowels, 1 vowel
    # plus 1 consonant, or 2 consonants.
    more_vowels, more_consonants = random.choice([(2, 0), (1, 1), (0, 2)])
    nvowels = 3 + more_vowels
    nconsonants = 4 + more_consonants
    letters = random.sample(vowels_pile, nvowels)
    letters += random.sample(consonants_pile, nconsonants)
    print_row(letters)
    seconds, score = clock.profile(letters_round, letters)
    print('Time:', seconds, 'seconds')
    return score


def play_numbers_round():
    large_numbers = [25, 50, 75, 100]
    small_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2
    numbers = random.sample(large_numbers + small_numbers, 6)
    target = random.randint(1, 999)
    # XXX A good test for the time spent in different strategies
    # numbers = [9, 1, 6, 4, 4, 25]
    # target = 773
    print_row([target])
    print_row(numbers)
    score1 = numbers_round(numbers, target, backtrack)
    print()
    score2 = numbers_round(numbers, target, bfs)
    return max(score1, score2)


def play_conundrum_round():
    print_row('CONUNDRUM')
    clue = ''.join(random.choice(conundrums.keys()))
    print_row(clue)
    seconds, answer = clock.profile(conundrum, clue)
    print('Time:', seconds, 'seconds')
    if answer:
        return 10
    return 0


def print_score(score):
    print('\nSCORE:', score, '\n')


def play_random_game():
    score = 0
    print_score(score)
    for section in range(2):
        for _ in range(4):
            score += play_letters_round()
            print_score(score)
        score += play_numbers_round()
        print_score(score)
    for _ in range(3):
        score += play_letters_round()
        print_score(score)
    score += play_numbers_round()
    print_score(score)
    score += play_conundrum_round()
    print_score(score)


if __name__ == '__main__':
    play_random_game()
