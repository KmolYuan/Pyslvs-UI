# -*- coding: utf-8 -*-

"""This module will test the functions of Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

import unittest
from unittest import TestCase

"""For necessary modules."""

class LibsTest(TestCase):
    
    """Testing Cython libs."""
    
    def test_topo(self):
        from core.libs import topo, Graph
        G = Graph([(0, 1), (0, 4), (1, 5), (2, 3), (2, 4), (3, 5), (4, 5)])
        H = Graph([(0, 2), (0, 4), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)])
        I = Graph([(0, 1), (0, 2), (1, 4), (2, 5), (3, 4), (3, 5), (4, 5)])
        self.assertTrue(G.is_isomorphic(H))
        self.assertFalse(G.is_isomorphic(I))
        answer, time = topo([4, 2], degenerate=True)
        self.assertEqual(len(answer), 2)
    
    def test_triangulation(self):
        from core.libs import auto_configure
        from networkx import Graph
        #Test for 8-bar linkage.
        G = Graph([(0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 4), (3, 5),
            (3, 7), (4, 6), (6, 7)])
        cus = {'P10': 7}
        same = {2: 1, 4: 3, 6: 7}
        status = {
            0: True,
            1: True,
            2: True,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False
        }
        pos = {
            0: (36.5, -59.5),
            1: (10.0, -94.12),
            2: (-28.5, -93.5),
            3: (102.5, -43.5),
            4: (77.5, -74.5),
            5: (28.82, -22.35),
            6: (23.5, 22.5),
            7: (-18.5, -44.5),
            8: (-75.5, -59.5),
            9: (56.5, 29.5),
            10: (68.5, 71.5),
            11: (-47.06, -28.24),
            12: (107.5, 42.5),
            13: (-109.41, -49.41),
            14: (44.12, 107.65)
        }
        Driver_list = ['P0']
        expr = auto_configure(G, cus, same, status, pos, Driver_list)
        self.assertEqual(len(expr), 6)
        for i, e in enumerate(expr):
            if i==0:
                self.assertEqual(e[0], 'PLAP')
            else:
                self.assertEqual(e[0], 'PLLP')

if __name__=='__main__':
    unittest.main()
