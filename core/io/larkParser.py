# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang
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
from core.graphics import colorName

#Get from parenthesis
get_from_parenthesis = lambda s, front, back: s[s.find(front)+1:s.find(back)]
get_front_of_parenthesis = lambda s, front: s[:s.find(front)]

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

common = common_NUMBER + common_CNAME + common_WS

COLOR_LIST = " | ".join("\"{}\"".format(color) for color in reversed(colorName()))

#Usage: tree = parser.parse(expr)
PMKS_parser = Lark(
    common +
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

#Usage: tree = parser.parse(expr)
#       pointsArgs = ArgsTransformer().transform(tree)
#       pointsArgs: Dict[str: value, ...]
class PMKSArgsTransformer(Transformer):
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

#Triangle expression parser.
triangle_parser = Lark(
    common +
    '''
    FUNCTIONTYPE: "PLAP" | "PLLP" | "PLPP"
    letter      : UCASE_LETTER+
    
    function    : FUNCTIONTYPE+
    link        : "L" INT
    angle       : "a" INT
    joint1      : "P" INT
    joint2      : letter (letter)*
    joint       : joint1 | joint2
    
    param       : angle | link | joint
    params      : param ("," param)*
    expr        : function "[" params "]" "(" joint ")"
    exprs       : expr (";" expr)*
    
    %ignore WS
    ''', start='exprs'
)

#tree = triangle_parser.parse("PLAP[A,L0,a0,B](C);PLLP[C,L1,L2,B](D);PLLP[C,L3,L4,D](E)")

#Turn into tuple format.
#TriangleArgsTransformer().transform(tree)
class TriangleArgsTransformer(Transformer):
    letter = lambda self, n: str(n[0])
    joint1 = lambda self, n: 'P{}'.format(n[0])
    joint2 = letter
    joint = letter
    link = lambda self, n: 'L{}'.format(n[0])
    angle = lambda self, n: 'a{}'.format(n[0])
    function = letter
    param = letter
    params = lambda self, a: tuple(a)
    expr = params
    exprs = params

#(('PLAP', ('A', 'L0', 'a0', 'B'), 'C'), ('PLLP', ('C', 'L1', 'L2', 'B'), 'D'), ...)
def triangle_expr(expr):
    tf = TriangleArgsTransformer()
    for func, params, target in tf.transform(triangle_parser.parse(expr)):
        yield func, params, target

#Return the symble by types.
#TriangleExprClassification().transform(tree)
class TriangleExprClassification(Transformer):
    def __init__(self):
        super(TriangleExprClassification, self).__init__()
        self.angles = []
        self.links = []
    
    def transform(self, tree):
        super(TriangleExprClassification, self).transform(tree)
        return tuple(sorted(self.angles)), tuple(sorted(self.links))
    
    def link(self, n):
        t = 'L{}'.format(n[0])
        if t not in self.links:
            self.links.append(t)
    
    def angle(self, n):
        t = 'a{}'.format(n[0])
        if t not in self.angles:
            self.angles.append(t)

def triangle_class(expr):
    tc = TriangleExprClassification()
    tmp_set = set()
    for func, params, target in triangle_expr(expr):
        tmp_set.add(target)
        for p in params:
            tmp_set.add(p)
    angles, links = tc.transform(triangle_parser.parse(expr))
    joints = tuple(sorted(tmp_set - set(angles) - set(links)))
    return angles, links, joints
