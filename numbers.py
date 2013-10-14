from __future__ import print_function
import countdown.clock as clock
from collections import deque
import timeit

operators = ('+', '*', '-', '/')

def numbers_round(numbers, target):
    formulate = 'print(%s(map(str, {}), {}))'.format(numbers, target)
    import_ = 'from __main__ import backtrack_formulate, bfs_formulate'
    backtrack = timeit.Timer(formulate % 'backtrack_formulate', import_)
    bfs = timeit.Timer(formulate % 'bfs_formulate', import_)
    print('\nTime (backtrack):', backtrack.timeit(number=1), 'seconds\n')
    print('\nTime (bfs):      ', bfs.timeit(number=1), 'seconds\n')

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
    clock.start()
    try:
        return backtrack(formulae)
    except clock.TimeIsUp:
        print('Could only find', eval(best_so_far.value))
        return best_so_far.value
    finally:
        clock.reset()

def bfs_formulate(formulae, target):
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
        print('Could only find', eval(best_so_far))
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
