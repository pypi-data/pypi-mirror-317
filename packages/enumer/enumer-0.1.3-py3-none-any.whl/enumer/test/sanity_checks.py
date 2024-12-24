# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@author   : Astrageldon
@contact  : astrageldon@gmail.com
@created  : 2024-12-23 17:33
@modified : 2024-12-24 17:02
-------------------------------------------------
"""


from enumer import *


def _test1():
    """
        Sanity check of the consistency between `enumer`
        with a tail oracle and `tail_enumer`.
    """
    mod = 1145141919810893_133713371337 ** 4 * 100000000
    flag = b'flag{super-easy_4nd_s7up!D_m@th_:D}' + b' '*16
    ct = b2l(flag) % mod
    tail = b' '*8
    target = list(enumer(ct, mod, max_length = len(flag), oracle = tail_oracle_factory(tail)))
    test = list(tail_enumer(ct, mod, tail, max_length = len(flag)))
    assert test == target
    print(len(target))
    for i in target:
        print(l2b(i))

def _test2():
    """
        Sanity check of the consistency between `enumer`
        with a tail oracle and `tail_enumer`.
    """
    mod = 1145
    flag = b'a' * 4
    tail = b'aa'
    ct = b2l(flag) % mod
    target = list(enumer(ct, mod, max_length = len(flag), oracle = tail_oracle_factory(tail)))
    test = list(tail_enumer(ct, mod, tail, max_length = len(flag)))
    assert test == target
    print(len(target))
    for i in target:
        print(l2b(i))

def _test3():
    """
        Sanity check of a `tail_enumer` that filters out
        certain elements.
    """
    mod = 1145141919810893_133713371337 ** 4
    flag = b'flag{super-easy_4nd_s7up!D_m@th_:D}' + b' '*16
    ct = b2l(flag) % mod
    tail = b' '*4
    print(l2b(next(tail_enumer(ct, mod, tail, max_length = len(flag), oracle = head_oracle_factory(b'flag{')))))

def _test4():
    """
        Sanity check of a `tail_enumer` that filters out
        certain elements.
    """
    mod = 1145141919810893_133713371337 ** 4
    flag = b'flag{super-easy_4nd_s7up!D_m@th_:D}' + b' '*12 + b'abcd'
    ct = b2l(flag) % mod
    tail = b2l(b'bcd') | (b'a'[0] & 0x1F) << 24
    print(l2b(next(tail_enumer(ct, mod, tail, max_length = len(flag), oracle = head_oracle_factory(b'flag{')))))

def _test5():
    """
        Sanity check of a `tail_enumer` that fails to
        find any eligible candidates.
    """
    mod = 1145141919810893_133713371337 ** 4
    flag = b'flag{super-easy_4nd_s7up!D_m@th_:D}' + b'a'*16
    ct = b2l(flag) % mod
    tail = b2l(b'a'*10) | (b'b'[0] & 0x1F) << 10 * 8
    try:
        print(l2b(next(tail_enumer(ct, mod, tail, max_length = len(flag), oracle = head_oracle_factory(b'flag{')))))
    except StopIteration:
        return
    raise ValueError

def _test6():
    """
        Sanity check of a `tail_enumer` that fails to
        find any eligible candidates.
    """
    mod = 1145141919810893_133713371337 ** 4 * 100000000
    flag = b'flag{super-easy_4nd_s7up!D_m@th_:D}' + b' '*16
    ct = b2l(flag) % mod
    tail = b'qxoxasxmxkmc'
    try:
        print(l2b(next(tail_enumer(ct, mod, tail, max_length = len(flag)))))
    except AssertionError:
        return
    raise ValueError

def _test7():
    """
        Sanity check of a `head_tail_enumer`.
    """
    mod = 1145141919810893_133713371337 ** 3 * 1100000000000000000000
    flag = b'flag{super-easy_4nd_s7up!D_m@th_:D}' + b' '*16
    ct = b2l(flag) % mod
    tail = b' '*6
    head = b'flag{'
    for i in head_tail_enumer(ct, mod, head, tail, len(flag)):
        print(l2b(i))

def _test8():
    """
        In comparison with the `tail_enumer` in `_test9`.
    """
    mod = 1145141919810893_133713371337 ** 7 * 100000000000000000000000000
    flag = b'- Hey buddy, you get the wrong door;   3fh9(*@UDHU(DUur93ioojdoiedwndi#D(*EwnjncnnjnO@e    the leather club is two blocks down.    - fuck you!'
    ct = b2l(flag) % mod
    tail = b'the leather club is two blocks down.    - fuck you!'
    head = b'- Hey buddy, you get the wrong door;'
    for i in head_tail_enumer(ct, mod, head, tail, len(flag)):
        print(l2b(i))

def _test9():
    """
        In comparison with the `head_tail_enumer` in `_test8`.
    """
    mod = 1145141919810893_133713371337 ** 7 * 100000000000000000000000000
    flag = b'- Hey buddy, you get the wrong door;   3fh9(*@UDHU(DUur93ioojdoiedwndi#D(*EwnjncnnjnO@e    the leather club is two blocks down.    - fuck you!'
    ct = b2l(flag) % mod
    tail = b'  the leather club is two blocks down.    - fuck you!'
    head = b'- Hey buddy, you get the wrong door;'
    for i in tail_enumer(ct, mod, tail, max_length = len(flag), oracle = head_oracle_factory(head)):
        print(l2b(i))

def _test10():
    """
        In comparison with the `tail_enumer` in `_test11`.
    """
    mod = 1145141919810893_133713371337 ** 4
    flag = b'ooh eeh ooh ah-ah  7!ng_t@nG_W4La_wa1A_6Ing_b@ng  oo eeh ooh ah-ah tingtangwalawalabingbang~'
    ct = b2l(flag) % mod
    tail = b'oo eeh ooh ah-ah tingtangwalawalabingbang~'
    head = b'ooh eeh ooh ah-ah'
    for i in head_tail_enumer(ct, mod, head, tail, len(flag), head_oracle_factory(head)):
        print(l2b(i))

def _test11():
    """
        In comparison with the `head_tail_enumer` in `_test10`.
    """
    mod = 1145141919810893_133713371337 ** 4
    flag = b'ooh eeh ooh ah-ah  7!ng_t@nG_W4La_wa1A_6Ing_b@ng  oo eeh ooh ah-ah tingtangwalawalabingbang~'
    ct = b2l(flag) % mod
    tail = b'oo eeh ooh ah-ah tingtangwalawalabingbang~'
    head = b'ooh eeh ooh ah-ah'
    bits = 0
    oracle = head_oracle_factory(head)
    for i in tail_enumer(ct, mod, tail, max_length = len(flag), oracle = true_factory()):
        if bits >= 720: break
        if i.bit_length() > bits:
            bits = i.bit_length()
            print(bits, b2l(flag).bit_length())
        if oracle(i):
            raise ValueError
        

def run_tests():
    for i in [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11
    ]:
        print(f'test{i}'.center(40, '='))
        exec(f'_test{i}()')
        print('success~')
