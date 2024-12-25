

if __name__ == '__main__':
    from operations import *

else:
    from mynewlib1.math.operations import *





def test_factorial(comments=True):
    if comments:
        print('test factorial...')
        print('.')
        print('.')
    assert factorial(3) == 6
    assert factorial(4) == 24
    if comments:
        print('factorial completed')

def test_permutation(comments=True):
    if comments:
        print('test permutation...')
        print('.')
        print('.')
    assert permutation(4) == 24

    if comments:
        print('permutation completed')

def test_compination(comments=True):
    if comments:
        print('test compination...')
        print('.')
        print('.')
    assert compination(5,3) == 10

    if comments:
        print('compination completed')

def test_binkof(comments=True):
    if comments:
        print('test binkof...')
        print('.')
        print('.')
    assert binkof(100,2) == 4950

    if comments:
        print('binkof completed')

def test_gamma(comments=True):
    if comments:
        print('test gamma...')
        print('.')
        print('.')
    assert gamma(4) == 6

    if comments:
        print('gamma completed')

def test_summaf(comments=True):
    if comments:
        print('test 5...')
        print('.')
        print('.')
    assert summaf(3) == 9

    if comments:
        print('summaf completed')

test_factorial()
test_permutation()
test_compination()
test_binkof()
test_gamma()
test_summaf()




