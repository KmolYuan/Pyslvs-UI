# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from lark import Lark, Transformer
from ..graphics.color import colorName

#Parenthesis
get_from_parenthesis = lambda s, front, back: s[s.find(front)+1:s.find(back)]

#Common grammar
common_NUMBER = '''
    DIGIT: "0".."9"
    INT: DIGIT+
    SIGNED_INT: ["+"|"-"] INT
    DECIMAL: INT "." INT? | "." INT
    _EXP: ("e"|"E") SIGNED_INT
    FLOAT: INT _EXP | DECIMAL _EXP?
    NUMBER: FLOAT | INT
'''
common_CNAME = '''
    LCASE_LETTER: "a".."z"
    UCASE_LETTER: "A".."Z"
    LETTER: UCASE_LETTER | LCASE_LETTER
    CNAME: ("_"|LETTER) ("_"|LETTER|DIGIT)*
'''
common_WS = '''
    WS: /[ \\t\\f\\r\\n]/+
'''

COLOR_LIST = " | ".join("\"{}\"".format(color) for color in reversed(colorName()))

parser = Lark(
    common_NUMBER + common_CNAME + common_WS +
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
    COLOR    : '''+COLOR_LIST+'''
    
    %ignore WS
    ''', start='mechanism'
)

class ArgsTransformer(Transformer):
    type = lambda self, n: str(n[0])
    name = type
    color = type
    neg = lambda self, n: -n[0]
    number = lambda self, n: float(n[0])
    point = lambda self, c: tuple(c)
    angle = number
    
    #Sort the argument list.
    def joint(self, args):
        '''
        [0]: type
        [1]: angle
        [1]/[2]: color
        [-2]: point
        [-1]: link
        '''
        hasAngle = args[0]!='R'
        color = args[2] if hasAngle else args[1]
        pointArgs = [
            ','.join(args[-1]),
            '{}:{}'.format(args[0], args[1]) if hasAngle else 'R',
            color if color in colorName() else 'Blue' if 'ground' in args[-1] else 'Green',
            args[-2][0],
            args[-2][1]
        ]
        return pointArgs
    
    link = lambda self, a: tuple(a)
    mechanism = lambda self, j: j
