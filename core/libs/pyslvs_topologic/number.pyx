# -*- coding: utf-8 -*-

"""Number synthesis."""

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from itertools import product

cdef inline int Max(int NL, int NJ):
    """
    + NL <= NJ and NJ <= (2*NL - 3)
    + (2*NL - 3) <= NJ and NJ <= (NL*(NL - 1)/2)
    + other exceptions (return -1).
    """
    if NL <= NJ and NJ <= (2*NL - 3):
        return NJ - NL + 2
    if NL == NJ == 0:
        return -1
    if (2*NL - 3) <= NJ and NJ <= (NL*(NL - 1)/2):
        return NL - 1
    return -1

cpdef object NumberSynthesis(int NL, int NJ):
    cdef list result = []
    cdef int Mmax = Max(NL, NJ)
    if Mmax == -1:
        return "incorrect mechanism."
    cdef int i, p
    cdef tuple symbols, answer
    for symbols in product(range(NL + 1), repeat=(Mmax - 2)):
        NLMmax = NL - sum(symbols)
        if NLMmax < 0:
            continue
        answer = symbols + (NLMmax,)
        if sum_factors(answer) == 2*NJ:
            result.append(answer)
    return tuple(result)

cdef inline int sum_factors(tuple factors):
    """
    F0*N2 + F1*N3 + F2*N4 + ... + Fn*N(n+2)
    """
    cdef int factor = 0
    for i, f in enumerate(factors):
        factor += f*(i + 2)
    return factor
