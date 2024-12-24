
if __name__ == '__main__':
    from progressions import *
else:
    from math_formulas.progressions.progressions import *

def test_algebric_progression_part():
    assert algebric_progression_part(1,3,5) == 13
    assert algebric_progression_part(5,8,4) == 29
    assert algebric_progression_part(11,25,32) == 786

def test_algebric_progression_sum():
    assert algebric_progression_sum(1,3,5) == 35
    assert algebric_progression_sum(5,8,4) == 68
    assert algebric_progression_sum(11,25,32) == 12752

def test_geometric_progression_part():
    assert geometric_progression_part(1,2,3) == 4
    assert geometric_progression_part(5,5,5) == 3125
    assert geometric_progression_part(3,4,4) == 192

def test_geometric_progression_sum():
    assert geometric_progression_sum(1,2,3) == 7
    assert geometric_progression_sum(5,5,5) == 3905
    assert geometric_progression_sum(3,4,4) == 255

test_algebric_progression_part()
test_algebric_progression_sum()
test_geometric_progression_part()
test_geometric_progression_sum()