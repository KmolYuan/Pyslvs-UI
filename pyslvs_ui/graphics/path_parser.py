# -*- coding: utf-8 -*-

"""Lark parser to parse the ambiguous path."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, Tuple, List, Union
from lark import Lark, Transformer, Tree

_GRAMMAR = Lark(r"""
// Number
DIGIT: "0".."9"
INT: DIGIT+
SIGNED_INT: ["+" | "-"] INT
DECIMAL: INT "." INT? | "." INT
_EXP: ("e" | "E") SIGNED_INT
FLOAT: INT _EXP | DECIMAL _EXP?
NUMBER: FLOAT | INT
SIGNED_NUMBER: ["+" | "-"] NUMBER
number: SIGNED_NUMBER

// White space and new line
WS: /[ \t]+/
CR: /\r/
LF: /\n/
_NEWLINE: (CR? LF)+
%ignore WS

// Main grammar
coord: number ","? number
?coord_style: "[" coord "]" | "(" coord ")" | coord
line: (coord_style (";" | ",")? _NEWLINE*)+
?start: line
""", parser='lalr')


class _Transformer(Transformer):
    """Transform into 2D coordinates data."""

    @staticmethod
    def number(n: List[str]) -> float:
        return float(n[0])

    @staticmethod
    def complex(n: List[str]) -> float:
        return float(n[0][:-1])

    @staticmethod
    def coord(n: Tuple[float, Union[float, Tree]]) -> Tuple[float, float]:
        if isinstance(n[1], float):
            return n[0], n[1]
        else:
            return n[0], float(cast(str, n[1].children[0]))

    @staticmethod
    def line(n):
        return n


_translator = _Transformer()


def parse_path(path: str) -> List[Tuple[float, float]]:
    """Parse path from csv."""
    return _translator.transform(_GRAMMAR.parse(path))
