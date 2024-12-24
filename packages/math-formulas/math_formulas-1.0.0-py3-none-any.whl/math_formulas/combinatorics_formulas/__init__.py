
if __name__ == '__main__':
    from combinatorics import *
else:
    from math_formulas.combinatorics_formulas.combinatorics import *

def test_combination():
    assert combination(4,2) == 6
    assert combination(10,7) == 120
    assert combination(15,10) == 3003

def test_placing():
    assert placing(4,2) == 12
    assert placing(10,7) == 604800
    assert placing(15,10) == 10897286400

def test_permutation():
    assert permutation(5) == 120
    assert permutation(8) == 40320
    assert permutation(10) == 3628800


test_combination()
test_placing()
test_permutation()