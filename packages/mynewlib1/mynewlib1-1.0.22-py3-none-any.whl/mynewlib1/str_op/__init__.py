
if __name__ == '__main__':
    from strop import *

else:
    from mynewlib1.str_op.strop import *


def test_single_number(comments=True):
    if comments:
        print('test_single_number ...')
    assert Task.evaluate('8')==8
    print('.')
    print('.')
    print('.')
    if comments:
        print('test_single_number completed')

def test_addition(comments=True):
    if comments:
        print('test_addition ...')
    assert Task.evaluate('8 + 8')==16
    print('.')
    print('.')
    print('.')
    if comments:
        print('test_addition completed')

def test_multiplication(comments=True):
    if comments:
        print('test_multiplication ...')
    assert Task.evaluate('3*4')==12
    print('.')
    print('.')
    print('.')
    if comments:
        print('test_multiplication completed')

def test_division(comments=True):
    if comments:
        print('test_division ...')
    assert Task.evaluate('10/2') == 5
    print('.')
    print('.')
    print('.')
    if comments:
        print('test_division completed')

