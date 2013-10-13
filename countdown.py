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


__all__ = ['letters_round', 'numbers_round', 'teaser', 'conundrum']

words = [w.strip() for w in open('/usr/share/dict/words').readlines()]
words = [w for w in words if len(w) <= len('countdown')]

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

operators_by_popularity = ('+', '*', '-', '/')

def numbers_round(numbers, target):
    print(formulate(map(str, numbers), target))

def formulate(formulae, target):
    answer = next((f for f in formulae if eval(f) == target), None)
    if answer:
        return answer
    for i1, f1 in enumerate(formulae):
        for i2, f2 in enumerate(formulae):
            if i1 == i2:
                continue
            for op in operators_by_popularity:
                if op == '+' and (i1 > i2 or eval(f1) == 0 or eval(f2) == 0):
                    continue
                if op == '-' and eval(f2) == 0:
                    continue
                if op == '*' and (i1 > i2 or eval(f1) == 1 or eval(f2) == 1):
                    continue
                if op == '/' and (eval(f2) == 1 or not divisible(f1, f2)):
                    continue
                new_formulae = combine(op, formulae, i1, i2)
                possible_answer = formulate(new_formulae, target)
                if possible_answer:
                    return possible_answer

def combine(op, formulae, index1, index2):
    combined = [f for i, f in enumerate(formulae) if i not in (index1, index2)]
    combined.append('(%s %s %s)' % (formulae[index1], op, formulae[index2]))
    return combined

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
    import random
    large_numbers = [25, 50, 75, 100]
    small_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2
    numbers = random.sample(large_numbers + small_numbers, 6)
    target = random.randint(1, 999)
    print_row(40, [target])
    print_row(40, numbers)
    numbers_round(numbers, target)


if __name__ == '__main__':
    play_numbers_round()
