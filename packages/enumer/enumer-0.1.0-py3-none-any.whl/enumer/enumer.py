# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@author   : Astrageldon
@contact  : astrageldon@gmail.com
@created  : 2024-12-23 17:33
@modified : 2024-12-23 17:33
-------------------------------------------------
"""


from .db import *



MITM_SIZE_LIMIT = 10000000



def tail_oracle_factory(tail: bytes):
    """
        An oracle factory manufacturing judgers that
        attempt to match the last bits of an input
        with `tail`.
       
    Args:
      tail (bytes):
        The targeted last few bits.

    Returns:
        A function that returns `True` if and only if
        the tail bits are match with `tail`.
    """
    taili = b2l(tail)
    l = len(tail) * 8
    mask = (1 << l) - 1
    return lambda n: n & mask == taili


def head_oracle_factory(head: bytes):
    """
        An oracle factory manufacturing judgers that
        attempt to match the first bits of an input
        with `head`.
       
    Args:
      head (bytes):
        The targeted first few bits.
        Must be non-degenerate, that is, free from
        leading `\x00`'s and non-empty.

    Returns:
        A function that returns `True` if and only if
        the head bits are match with `head`.
    """
    l = len(head)
    assert not head.startswith(b'\0') and l > 0, "Degenerate head."
    headi = b2l(head)
    return lambda n: n > 0 and n >> max(((n.bit_length() + 7) // 8 - l) * 8, 0) == headi


def true_factory():
    """
        A constant oracle factory.

    Returns:
        A function that always returns `True`.
    """
    return lambda *_, **__: True


def false_factory():
    """
        A constant oracle factory.

    Returns:
        A function that always returns `False`.
    """
    return lambda *_, **__: False



def enumer(rem: int, mod: int, max_length: int = None, upper_bound: int = None, oracle: Callable = true_factory()):
    """
        Ordinary residue class enumerator. That is,
        for each non-negative integer `k`, those of the form
        `rem + k * mod` that make the oracle come true.
       
    Args:
      rem (int):
        A representative of a residue class modulo `mod`.
      
      mod (int):
        The modulus.
      
    Keyword Args:
      max_length (int):
        (Mutually exclusive with `upper_bound`). Unlimited by default.
        Specifies the maximum length of an residue class element
        to be enumerated as an MSB byte sequence.
      
      upper_bound (int):
        (Mutually exclusive with `max_length`). Unlimited by default.
        Specifies the upper limit of an residue class element
        to be enumerated as an integer.
      
      oracle (Callable):
        (An oracle that always returns `True` by default).
        A judger for each residue class element on whether a candidate
        representative should be output or not.

    Returns:
        A generator used for exhaustive enumeration.
    """
    assert not (max_length != None and upper_bound != None), "Ambiguous upper bounds."
    ub = None
    if max_length != None:
        ub = 1 << (max_length << 3)
    elif upper_bound != None:
        ub = upper_bound
    while max_length is None or rem.bit_length() <= max_length * 8:
        if oracle(rem):
            yield rem
        rem += mod


def tail_enumer(rem: int, mod: int, tail: [bytes, int], max_length: int = None, upper_bound: int = None, tail_bit_length: int = None, oracle: Callable = true_factory()):
    """
        Residue class enumerator with partial tail
        information given.
        A main difference from the ordinary one
        is that, an enumerator could work more efficiently
        when given some tail bits.
       
    Args:
      rem (int):
        A representative of a residue class modulo `mod`.
      
      mod (int):
        The modulus.
      
      tail (bytes / int):
        The last few bits that each output must possess.
      
    Keyword Args:
      max_length (int):
        (Mutually exclusive with `upper_bound`). Unlimited by default.
        Specifies the maximum length of an residue class element
        to be enumerated as an MSB byte sequence.
      
      upper_bound (int):
        (Mutually exclusive with `max_length`). Unlimited by default.
        Specifies the upper limit of an residue class element
        to be enumerated as an integer.
      
      tail_bit_length (int):
        (Only used when `tail` is of type `int`). The number of bits
        (counting from the leading 1) in `tail`.
        The exact number of the demanded tail bits.
      
      oracle (Callable):
        (An oracle that always returns `True` by default).
        A judger for each residue class element on whether a candidate
        representative should be output or not.

    Returns:
        A generator used for exhaustive enumeration given tail bits.
    """
    assert not (max_length != None and upper_bound != None), "Ambiguous upper bounds."
    if isinstance(tail, bytes):
        assert tail_bit_length is None, "Ambiguous length specification."
        l = len(tail) << 3
        taili = b2l(tail)
    elif isinstance(tail, int):
        l = tail.bit_length() if tail_bit_length is None else tail_bit_length
        taili = tail
    else:
        raise TypeError
    g = gcd(2**l, mod)
    assert (taili - rem) % g == 0, "Impossible tail."
    stride1 = (taili - rem)//g * pow(mod//g, -1, 2**l//g) % (2**l//g)
    stride1 *= mod
    stride2 = mod * 2**l // g
    rem += stride1
    ub = None
    if max_length != None:
        ub = 1 << (max_length << 3)
    elif upper_bound != None:
        ub = upper_bound
    while ub is None or rem <= ub:
        if oracle(rem):
            yield rem
        rem += stride2


def _F(x, L):
    return x - (x & ((1 << L) - 1))


def _Delta(a, b, L):
    return 1 if (a & ((1 << L) - 1)) + (b & ((1 << L) - 1)) >= 1 << L else 0


def head_tail_enumer(rem: int, mod: int, head: bytes, tail: bytes, length: int, oracle: Callable = true_factory(), size_limit = MITM_SIZE_LIMIT):
    """
        Residue class enumerator with partial information
        of both first few and last few bits.
        This method is faster, but may fail due to
        space limitations (even when enough head bits
        are provided).
       
    Args:
      rem (int):
        A representative of a residue class modulo `mod`.
      
      mod (int):
        The modulus.
      
      head (bytes):
        The first few bits that each output must possess.
        Must be non-degenerate, that is, free from leading `\x00`'s
        and non-empty.
      
      tail (bytes):
        The last few bits that each output must possess.
      
      length (int):
        The exact length of each output as an MSB byte sequence.
      
    Keyword Args:
      oracle (Callable):
        (An oracle that always returns `True` by default).
        A judger for each residue class element on whether a candidate
        representative should be output or not.
      
      size_limit (int):
        (`MITM_SIZE_LIMIT` by default).
        The upper limit for the size of the meet-in-the-middle trick.
        If the number of table entries needed exceeds `size_limit`, the
        enumeration will be aborted.

    Returns:
        A generator used for exhaustive enumeration given
        both head and tail bits.
    """
    lr = len(tail) << 3
    ll = len(head) << 3
    L = length << 3
    assert lr + ll <= L and rem < 2**L, "Wrong length(s)."
    assert not head.startswith(b'\0') and ll > 0, "Degenerate head."
    taili = b2l(tail)
    headi = b2l(head) << L - ll
    g = gcd(2**lr, mod)
    assert (taili - rem) % g == 0, "Impossible tail."
    stride1 = (taili - rem)//g * pow(mod//g, -1, 2**lr//g) % (2**lr//g)
    stride1 *= mod
    stride2 = mod * 2**lr // g
    rem += stride1
    D2 = ((1 << L) - rem + stride2 - 1) // stride2
    D = isqrt(D2)
    if D > size_limit:
        raise ValueError("(%d > %d) table entries needed." % (D, size_limit))
    table = {}
    for K1 in range(D, -1, -1):
        n = rem + K1 * D * stride2
        if n < 1 << L - ll: break
        for d in range(2):
            k = headi - _F(K1 * D * stride2, L - ll) - (d << L - ll)
            table.update({k: table.get(k, []) + [(K1, d)]})
    for K2 in range(D):
        n = rem + K2 * stride2
        for K1, d in table.get(_F(n, L - ll), []):
            if _Delta(n, K1 * D * stride2, L - ll) == d:
                res = rem + (K1 * D + K2) * stride2
                assert l2b(res).startswith(head)
                yield res


