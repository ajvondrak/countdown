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

from operator import add, sub, mul, div

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
    return same_letters(word, letters) and enough_of_each_letter(word, letters)

def same_letters(word, letters):
    return set(word).issubset(set(letters))

def enough_of_each_letter(word, letters):
    return all(word.count(l) <= letters.count(l) for l in letters)

#####################
### Teaser        ###
#####################

def teaser(clue):
    for word in possible_words(clue):
        print(word)

#####################
### Numbers Round ###
#####################

operators_by_popularity = (add, mul, sub, div)

op_sym = {add:'+', sub:'-', mul:'*', div:'/'}

def numbers_round(numbers, target):
    return formulate(target, [(n, str(n)) for n in numbers])

def formulate(target, formulae):
    if any([number == target for number, formula in formulae]):
        return formula
    for index1 in range(len(formulae)):
        for index2 in range(len(formulae)):
            if index1 == index2:
                continue
            for op in operators_by_popularity:
                new_formulae = combine(op, formulae, index1, index2)
                possible_answer = formulate(target, new_formulae)
                if possible_answer:
                    return possible_answer

def combine(op, formulae, index1, index2):
    indices = (index1, index2)
    number1, formula1 = formulae[index1]
    number2, formula2 = formulae[index2]
    if op == div and not divisible(number1, number2):
        return []
    new_formulae = [f for i, f in enumerate(formulae) if i not in indices]
    new_number = op(number1, number2)
    new_formula = '(%s %s %s)' % (formula1, op_sym[op], formula2)
    new_formulae.append((new_number, new_formula))
    return new_formulae

def divisible(numerator, denominator):
    return denominator != 0 and numerator % denominator == 0

#####################
### Conundrum     ###
#####################

def conundrum(anagram):
    for word in words:
        if anagram == ''.join(sorted(word)):
            print(word)
