# -*- coding: utf-8 -*-

"""Lark parser to parse the expression.

+ PMKS
+ Triangular iteration
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from lark import Lark, Transformer
from typing import Dict, Union
from core.graphics import colorNames


_COLOR_LIST = " | ".join('"{}"'.format(color) for color in reversed(colorNames))

_pmks_parser = Lark(
    #Number
    """
    DIGIT: "0".."9"
    INT: DIGIT+
    SIGNED_INT: ["+"|"-"] INT
    DECIMAL: INT "." INT? | "." INT
    _EXP: ("e"|"E") SIGNED_INT
    FLOAT: INT _EXP | DECIMAL _EXP?
    NUMBER: FLOAT | INT
    """
    #Letters
    """
    LCASE_LETTER: "a".."z"
    UCASE_LETTER: "A".."Z"
    LETTER: UCASE_LETTER | LCASE_LETTER
    CNAME: ("_"|LETTER) ("_"|LETTER|DIGIT)*
    """
    #White space
    """
    WS: /[ \\t\\f\\r\\n]/+
    """
    #Main document.
    """
    type: JOINTTYPE+
    name: CNAME
    num : NUMBER  -> number
        | "-" num -> neg
    
    joint    : "J[" type ("," angle)? ("," color)? "," point "," link "]"
    link     : "L[" name ("," name)* "]"
    point    : "P[" num  "," num "]"
    angle    : "A[" num "]"
    colorv   : INT
    color    : "color[" (("(" colorv "," colorv "," colorv ")") | COLOR+) "]"
    mechanism: "M[" [joint ("," joint)*] "]"
    
    JOINTTYPE: "RP" | "R" | "P"
    COLOR    : """ + _COLOR_LIST + """
    
    %ignore WS
    """, start = 'mechanism'
)


class PMKSTransformer(Transformer):
    
    """Usage: tree = parser.parse(expr)
    
    args = transformer().transform(tree)
    args: Dict[str, value]
    """
    
    type = lambda self, n: str(n[0])
    name = type
    
    def color(self, n):
        if len(n) == 1:
            return str(n[0])
        else:
            return str(tuple(n))
    
    def colorv(self, n):
        return int(n[0])
    
    neg = lambda self, n: -n[0]
    number = lambda self, n: float(n[0])
    point = lambda self, c: tuple(c)
    angle = number
    
    def joint(self, args):
        """Sort the argument list.
        
        [0]: type
        [1]: angle
        [1]/[2]: color
        [-2]: point
        [-1]: link
        """
        hasAngle = args[0]!='R'
        color = args[2] if hasAngle else args[1]
        x, y = args[-2]
        pointArgs = [
            ','.join(args[-1]),
            '{}:{}'.format(args[0], args[1]) if hasAngle else 'R',
            color,
            x,
            y
        ]
        return pointArgs
    
    link = lambda self, a: tuple(a)
    mechanism = lambda self, j: j


def parse(expr: str) -> Dict[str, Union[int, float, str]]:
    """Using to parse the expression and return arguments."""
    return PMKSTransformer().transform(_pmks_parser.parse(expr))
