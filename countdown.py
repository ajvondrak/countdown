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
### Numbers Round ###
#####################

operators_by_popularity = ('+', '*', '-', '/')

def numbers_round(numbers, target):
    print(formulate(map(str, numbers), target))

def commutative(op):
    return op in ('+', '*')

def formulate(formulae, target):
    answer = next((f for f in formulae if eval(f) == target), None)
    if answer:
        return answer
    for index1 in range(len(formulae)):
        for index2 in range(len(formulae)):
            if index1 == index2:
                continue
            for op in operators_by_popularity:
                if commutative(op) and index1 > index2:
                    # Already computed an equivalent branch of the recursion
                    # tree back when index1 < index2
                    continue
                new_formulae = combine(op, formulae, index1, index2)
                possible_answer = formulate(new_formulae, target)
                if possible_answer:
                    return possible_answer

def combine(op, formulae, index1, index2):
    if op == '/' and not divisible(formulae[index1], formulae[index2]):
        return []
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
        if word == ''.join(sorted(anagram)):
            yield anagram

def teaser(clue):
    for anagram in anagrams(clue):
        print('It might be: ' + anagram)

def conundrum(word):
    print(next(anagrams(word)))
