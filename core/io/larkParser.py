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

parser = Lark(
    '''
    type: JOINTTYPE+
    name: CNAME
    num : NUMBER  -> number
        | "-" num -> neg
    
    joint    : "J[" [type ("," angle)? "," point "," link ("," num)?] "]"
    link     : "L[" [name ("," name)*] "]"
    point    : "P[" [num  "," num] "]"
    angle    : "A[" num "]"
    mechanism: "M[" [joint ("," joint)*] "]"
    
    JOINTTYPE: "RP" | "R" | "P"
    
    %import common.NUMBER
    %import common.CNAME
    %import common.WS
    %ignore WS
    ''', start='mechanism'
)

class ArgsTransformer(Transformer):
    type = lambda self, n: str(n[0])
    name = type
    neg = lambda self, n: -n[0]
    number = lambda self, n: float(n[0])
    point = lambda self, c: tuple(c)
    angle = number
    
    #Sort the argument list.
    def joint(self, args):
        pointArgs = [
            ','.join(args[-1]),
            '{}:{}'.format(args[0], args[1]) if args[0]!='R' else 'R',
            'Blue' if 'ground' in args[-1] else 'Green',
            args[-2][0],
            args[-2][1]
        ]
        return pointArgs
    
    link = lambda self, a: tuple(a)
    mechanism = lambda self, j: j

if __name__=='__main__':
    expr = "M[J[R, P[-10.,0.], L[ground, i]], J[R, P[-10.,0.], L[ground, link_0]]]"
    tree = parser.parse(expr)
    print(tree.pretty())
    print(ArgsTransformer().transform(tree))
