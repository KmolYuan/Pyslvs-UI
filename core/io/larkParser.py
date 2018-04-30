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
from core.graphics import colorName


_COLOR_LIST = " | ".join('"{}"'.format(color) for color in reversed(colorName))

#Usage: tree = parser.parse(expr)
PMKS_parser = Lark(
    #Number
    '''
    DIGIT: "0".."9"
    INT: DIGIT+
    SIGNED_INT: ["+"|"-"] INT
    DECIMAL: INT "." INT? | "." INT
    _EXP: ("e"|"E") SIGNED_INT
    FLOAT: INT _EXP | DECIMAL _EXP?
    NUMBER: FLOAT | INT
    '''
    #Letters
    '''
    LCASE_LETTER: "a".."z"
    UCASE_LETTER: "A".."Z"
    LETTER: UCASE_LETTER | LCASE_LETTER
    CNAME: ("_"|LETTER) ("_"|LETTER|DIGIT)*
    '''
    #White space
    '''
    WS: /[ \\t\\f\\r\\n]/+
    '''
    
    '''
    type: JOINTTYPE+
    name: CNAME
    num : NUMBER  -> number
        | "-" num -> neg
    
    joint    : "J[" [type ("," angle)? ("," color)? "," point "," link] "]"
    link     : "L[" [name ("," name)*] "]"
    point    : "P[" [num  "," num] "]"
    angle    : "A[" num "]"
    color    : "color[" COLOR+ "]"
    mechanism: "M[" [joint ("," joint)*] "]"
    
    JOINTTYPE: "RP" | "R" | "P"
    COLOR    : ''' + _COLOR_LIST + '''
    
    %ignore WS
    ''', start='mechanism'
)


class PMKSArgsTransformer(Transformer):
    
    """Usage: tree = parser.parse(expr)
    
    pointsArgs = ArgsTransformer().transform(tree)
    pointsArgs: Dict[str: value]
    """
    
    type = lambda self, n: str(n[0])
    name = type
    color = type
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
        if color not in colorName:
            color = 'Blue'
        elif 'ground' in args[-1]:
            color = 'Green'
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
