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
from pygments.lexer import RegexLexer
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
)
from typing import List, Union
from core.graphics import colorNames
from core.libs import VPoint


_COLOR_LIST = " | ".join('"{}"'.format(color) for color in reversed(colorNames))

_pmks_grammar = Lark(
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
    #White space and new line.
    """
    WS: /[ \\t\\f\\r\\n]/+
    CR : /\\r/
    LF : /\\n/
    NEWLINE: (CR? LF)+
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
    mechanism: "M[" [joint ("," joint)* (",")?] "]"
    
    JOINTTYPE: "RP" | "R" | "P"
    COLOR    : """ + _COLOR_LIST + """
    
    %ignore WS
    %ignore NEWLINE
    COMMENT: "#" /[^\\n]/*
    %ignore COMMENT
    """, start = 'mechanism'
)


class _PMKSParams(Transformer):
    
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
    
    colorv = lambda self, n: int(n[0])
    neg = lambda self, n: -n[0]
    number = lambda self, n: float(n[0])
    point = lambda self, c: tuple(c)
    angle = number
    link = lambda self, a: tuple(a)
    
    def joint(self, args):
        """Sort the argument list.
        
        [0]: type
        [1]: angle
        [1]/[2]: color
        [-2]: point
        [-1]: link
        """
        hasAngle = args[0] != 'R'
        x, y = args[-2]
        return [
            ','.join(args[-1]),
            '{}:{}'.format(args[0], args[1]) if hasAngle else 'R',
            args[2] if hasAngle else args[1],
            x,
            y
        ]
    
    mechanism = lambda self, j: j

class _PMKSVPoints(_PMKSParams):
    
    """Using same grammar return as VPoints."""
    
    type = lambda self, n: ('R', 'P', 'RP').index(str(n[0]))
    
    def joint(self, args):
        hasAngle = args[0] != 0
        x, y = args[-2]
        return VPoint(
            ','.join(args[-1]),
            args[0],
            args[1] if hasAngle else 0.,
            args[2] if hasAngle else args[1],
            x,
            y
        )


def parse_params(expr: str) -> List[List[Union[str, float]]]:
    """Using to parse the expression and return arguments."""
    return _PMKSParams().transform(_pmks_grammar.parse(expr))

def parse_vpoints(expr: str) -> List[VPoint]:
    """Parse as VPoints."""
    return _PMKSVPoints().transform(_pmks_grammar.parse(expr))


class PMKSLexer(RegexLexer):
    
    """PMKS highlighter by Pygments."""
    
    name = 'PMKS'
    
    tokens = {'root': [
        ('#.*$', Comment.Single),
        ('(M)|(J)|(L)|(P)|(A)|(color)', Name.Function),
        ('|'.join("({})".format(color) for color in colorNames), Name.Variable),
        ('(R)|(P)|(RP)', Keyword.Constant),
        (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
    ]}
