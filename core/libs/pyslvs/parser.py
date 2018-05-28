# -*- coding: utf-8 -*-

"""Lark parser to parse the expression.

+ PMKS
+ Triangular iteration
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Union,
)
from lark import Lark, Transformer
from lark.lexer import Token

try:
    from pygments.lexer import RegexLexer
    from pygments.token import (
        Comment,
        Keyword,
        Name,
        Number,
    )
except ImportError:
    HAS_PYGMENTS = False
else:
    HAS_PYGMENTS = True

from .tinycadlib import VPoint


#Color dictionary.
_color_list = {
    'Red': (172, 68, 68),
    'Green': (110, 190, 30),
    'Blue': (68, 120, 172),
    'Cyan': (0, 255, 255),
    'Magenta': (255, 0, 255),
    'Brick-Red': (255, 130, 130),
    'Yellow': (255, 255, 0),
    'Gray': (160, 160, 160),
    'Orange': (225, 165, 0),
    'Pink': (225, 192, 230),
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Dark-Red': (128, 0, 0),
    'Dark-Green': (0, 128, 0),
    'Dark-Blue': (0, 0, 128),
    'Dark-Cyan': (128, 0, 128),
    'Dark-Magenta': (255, 0, 255),
    'Dark-Yellow': (128, 128, 0),
    'Dark-Gray': (128, 128, 128),
    'Dark-Orange': (225, 140, 0),
    'Dark-Pink': (225, 20, 147),
}

colorNames = tuple(sorted(_color_list.keys()))

def colorRGB(name: str) -> Tuple[int, int, int]:
    """Get color by name.
    
    + Invalid color
    + Color key
    + RGB string.
    """
    if not name:
        return (0, 0, 0)
    elif name in _color_list:
        return _color_list[name]
    else:
        #Input RGB as a "(255, 255, 255)" string.
        return tuple(int(i) for i in (
            name.replace('(', '')
            .replace(')', '')
            .replace(" ", '')
            .split(',')
        ))

_colors = "|".join('"{}"'.format(color) for color in reversed(colorNames))

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
    COLOR    : """ + _colors + """
    
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
    
    def type(self, n: List[Token]) -> str:
        return str(n[0])
    
    name = type
    
    def color(self, n: List[Token]) -> str:
        return str(n[0]) if (len(n) == 1) else str(tuple(n))
    
    def colorv(self, n: List[Token]) -> int:
        return int(n[0])
    
    def neg(self, n: List[Token]) -> Token:
        return -n[0]
    
    def number(self, n: List[Token]) -> float:
        return float(n[0])
    
    def point(self, c: List[Token]) -> Tuple[Token]:
        return tuple(c)
    
    angle = number
    
    def link(self, a: List[Token]) -> Tuple[Token]:
        return tuple(a)
    
    def joint(self, args: List[Token]) -> List[Union[str, int, float]]:
        """Sort the argument list.
        
        [0]: type
        ([1]: angle)
        ([1])[2]: color
        ([2])[3]: point (coordinate)
        ([3])[4]: link
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
    
    def mechanism(self, j: List[Token]) -> List[Token]:
        return j

class _PMKSVPoints(_PMKSParams):
    
    """Using same grammar return as VPoints."""
    
    def type(self, n: List[Token]) -> int:
        """Return as int type."""
        return ('R', 'P', 'RP').index(str(n[0]))
    
    def joint(self, args: List[Token]) -> VPoint:
        """Same as parent."""
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

if HAS_PYGMENTS:
    
    class PMKSLexer(RegexLexer):
        
        """PMKS highlighter by Pygments."""
        
        name = 'PMKS'
        
        tokens = {'root': [
            ('#.*$', Comment.Single),
            ('(M)|(J)|(L)|(P)|(A)|(color)', Name.Function),
            ('|'.join("({})".format(color) for color in colorNames), Name.Variable),
            ('(RP)|(R)|(P)', Keyword.Constant),
            (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
        ]}
