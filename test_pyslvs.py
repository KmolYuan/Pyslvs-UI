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
from core.io import parse_vpoints
from core.libs import (
    Coordinate,
    PLAP,
    PLLP,
    PLPP,
    vpoints_configure,
    expr_solving,
    topo,
    Genetic,
    Firefly,
    DiffertialEvolution,
    Planar,
)


class LibsTest(TestCase):
    
    """Testing Cython libs."""
    
    def test_plap(self):
        """Test for PLAP function."""
        A = Coordinate(0, 0)
        B = Coordinate(50, 0)
        x, y = PLAP(A, 50*sqrt(2), radians(45), B)
        self.assertTrue(isclose(x, 50))
        self.assertTrue(isclose(y, 50))
    
    def test_pllp(self):
        """Test for PLLP function."""
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
    
    def test_plpp(self):
        """Test for PLPP function."""
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
    
    def test_solving(self):
        """Test triangular formula solving.
        
        + Test for PMKS parser.
        + Jansen's linkage (Single).
        """
        vpoints = parse_vpoints("M[\n" +
            "# Jansen's linkage (Single).\n" +
            "J[R, color[(255, 255, 255)], P[0.0, 0.0], L[ground, link_1]],\n" +
            "J[R, color[Green], P[9.61, 11.52], L[link_1, link_2, link_4]],\n" +
            "J[R, color[Blue], P[-38.0, -7.8], L[ground, link_3, link_5]],\n" +
            "J[R, color[Green], P[-35.24, 33.61], L[link_2, link_3]],\n" +
            "J[R, color[Green], P[-77.75, -2.54], L[link_3, link_6]],\n" +
            "J[R, color[Green], P[-20.1, -42.79], L[link_4, link_5, link_7]],\n" +
            "J[R, color[Green], P[-56.05, -35.42], L[link_6, link_7]],\n" +
            "J[R, color[Green], P[-22.22, -91.74], L[link_7]],\n" +
            "]")
        self.assertTrue(len(vpoints) == 8)
        x, y = expr_solving(
            vpoints_configure(vpoints, [(0, 1)]),
            {n: 'P{}'.format(n) for n in range(len(vpoints))},
            vpoints,
            [0.]
        )[-1]
        self.assertTrue(isclose(x, -43.17005515543241))
        self.assertTrue(isclose(y, -91.75322590542523))
    
    def planar_object(self):
        """Test-used mechanism for algorithm."""
        return Planar({
            'Driver': {'P0': (-70, -70, 50)},
            'Follower': {'P1': (70, -70, 50)},
            'Target': {'P4': [
                (60.3, 118.12),
                (31.02, 115.62),
                (3.52, 110.62),
                (-25.77, 104.91),
                (-81.49, 69.19),
                (-96.47, 54.906),
                (-109.34, 35.98),
                (-121.84, 13.83),
                (-127.56, -20.09),
                (-128.63, -49.74),
                (-117.56, -65.45),
            ]},
            'Expression': "PLAP[P0,L0,a0](P2);" +
                "PLLP[P2,L1,L2,P1](P3);" +
                "PLLP[P2,L3,L4,P3](P4)",
            'constraint': [('P0', 'P1', 'P2', 'P3')],
            'IMin': 5., 'LMin': 5.,
            'FMin': 5., 'AMin': 0.,
            'IMax': 100., 'LMax': 100.,
            'FMax': 100., 'AMax': 360.,
        })
    
    def test_algorithm_rga(self):
        """Real-coded genetic algorithm."""
        fun1 = Genetic(self.planar_object(), {
            'maxTime': 10, 'report': 10,
            #Genetic
            'nPop': 500,
            'pCross': 0.95,
            'pMute': 0.05,
            'pWin': 0.95,
            'bDelta': 5.,
        })
        fun1.run()
    
    def test_algorithm_firefly(self):
        """Firefly algorithm."""
        fun2 = Firefly(self.planar_object(), {
            'maxTime': 10, 'report': 10,
            #Firefly
            'n': 80,
            'alpha': 0.01,
            'betaMin': 0.2,
            'gamma': 1.,
            'beta0': 1.,
        })
        fun2.run()
    
    def test_algorithm_de(self):
        """Differtial evolution."""
        fun3 = DiffertialEvolution(self.planar_object(), {
            'maxTime': 10, 'report': 10,
            #DE
            'strategy': 1,
            'NP': 400,
            'F': 0.6,
            'CR': 0.9,
        })
        fun3.run()


if __name__ == '__main__':
    unittest.main()
