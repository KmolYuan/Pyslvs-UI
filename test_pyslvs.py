# -*- coding: utf-8 -*-

"""This module will test the functions of Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

import unittest
from unittest import TestCase

#For necessary modules.
from math import sqrt, radians, isclose
from core.libs import (
    VPoint,
    Coordinate,
    PLAP,
    PLLP,
    PLPP,
    vpoints_configure,
    expr_solving,
    topo,
    graph_configure,
)

class LibsTest(TestCase):
    
    """Testing Cython libs."""
    
    def test_PLAP(self):
        A = Coordinate(0, 0)
        B = Coordinate(50, 0)
        x, y = PLAP(A, 50*sqrt(2), radians(45), B)
        self.assertTrue(isclose(x, 50))
        self.assertTrue(isclose(y, 50))
    
    def test_PLLP(self):
        A = Coordinate(-30, 0)
        B = Coordinate(30, 0)
        x, y = PLLP(A, 50, 50, B)
        self.assertTrue(isclose(x, 0))
        self.assertTrue(isclose(y, 40))
        x, y = PLLP(A, 30, 30, B)
        self.assertTrue(isclose(x, 0))
        self.assertTrue(isclose(y, 0))
        x, y = PLLP(A, 90, 30, B)
        self.assertTrue(isclose(x, 60))
        self.assertTrue(isclose(y, 0))
    
    def test_PLPP(self):
        A = Coordinate(0, 0)
        B = Coordinate(0, -3)
        C = Coordinate(3/2, 0)
        x, y = PLPP(A, sqrt(5), B, C)
        self.assertTrue(isclose(x, 2))
        self.assertTrue(isclose(y, 1))
    
    def test_topologic(self):
        """Testing 'topologic' libraries.
        
        + 'topo' function.
        + 'Graph' class.
        """
        from core.libs import Graph
        G = Graph([(0, 1), (0, 4), (1, 5), (2, 3), (2, 4), (3, 5), (4, 5)])
        H = Graph([(0, 2), (0, 4), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)])
        I = Graph([(0, 1), (0, 2), (1, 4), (2, 5), (3, 4), (3, 5), (4, 5)])
        self.assertTrue(G.is_isomorphic(H))
        self.assertFalse(G.is_isomorphic(I))
        answer, time = topo([4, 2], degenerate=True)
        self.assertEqual(len(answer), 2)
    
    def test_triangulation1(self):
        """Testing 'triangulation' libraries.
        
        + 'graph_configure' function.
        + Start at P0. (Can not use A ... Z letter.)
        """
        from networkx import Graph
        #Test for 8-bar linkage.
        G = Graph([(0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 4), (3, 5),
            (3, 7), (4, 6), (6, 7)])
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
        cus = {'P10': 7}
        same = {2: 1, 4: 3, 7: 6}
        expr = graph_configure(G, status, pos, Driver_list, cus, same)
        self.assertEqual(len(expr), 6)
        for i, e in enumerate(expr):
            if i == 0:
                self.assertEqual(e[0], 'PLAP')
            else:
                self.assertEqual(e[0], 'PLLP')
        for node, n_status in status.items():
            self.assertFalse((not n_status) and (node not in same))
    
    def test_solving(self):
        """Test triangular formula solving.
        
        + Jansen's linkage (Single).
        """
        vpoints = [
            VPoint("ground, link_1", 0, 0., 'Green', 0., 0.),
            VPoint("link_1, link_2, link_4", 0, 0., 'Green', 9.61, 11.52),
            VPoint("ground, link_3, link_5", 0, 0., 'Blue', -38.0, -7.8),
            VPoint("link_2, link_3", 0, 0., 'Green', -35.24, 33.61),
            VPoint("link_3, link_6", 0, 0., 'Green', -77.75, -2.54),
            VPoint("link_4, link_5, link_7", 0, 0., 'Green', -20.1, -42.79),
            VPoint("link_6, link_7", 0, 0., 'Green', -56.05, -35.42),
            VPoint("link_7", 0, 0., 'Green', -22.22, -91.74),
        ]
        x, y = expr_solving(
            vpoints_configure(vpoints, [(0, 1)]),
            {n: 'P{}'.format(n) for n in range(len(vpoints))},
            vpoints,
            [0.]
        )[-1]
        self.assertTrue(isclose(x, -43.17005515543241))
        self.assertTrue(isclose(y, -91.75322590542523))

if __name__=='__main__':
    unittest.main()
