from __future__ import print_function
from collections import deque
import countdown.clock as clock


operators = ('+', '*', '-', '/')


def numbers_round(numbers, target, strategy):
    numbers = map(str, numbers)
    print('Using', strategy.__name__, 'strategy...')
    seconds, formula = clock.profile(strategy, numbers, target)
    number_reached = eval(formula)
    print(number_reached)
    print(formula)
    print('Time:', seconds, 'seconds')
    if number_reached == target:
        return 10
    elif abs(number_reached - target) <= 5:
        return 7
    elif abs(number_reached - target) <= 10:
        return 5
    else:
        return 0


def backtrack(formulae, target):
    # For lack of a `nonlocal` keyword in Python 2.x
    nonlocals = {'best_so_far':'0'}

    def formulate(formulae):
        closest = closest_to(target, formulae)
        if eval(closest) == target:
            return closest
        nonlocals['best_so_far'] = \
                closest_to(target, (nonlocals['best_so_far'], closest))
        for new_formulae in possible_formulae(formulae):
            answer = formulate(new_formulae)
            if answer:
                return answer

    clock.start()
    try:
        return formulate(formulae)
    except clock.TimeIsUp:
        return nonlocals['best_so_far']
    finally:
        clock.reset()


def bfs(formulae, target):
    best_so_far = '0'
    formulae = tuple(formulae)
    visited = set([formulae])
    worklist = deque([formulae])
    clock.start()
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
    except clock.TimeIsUp:
        return best_so_far
    finally:
        clock.reset()


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
