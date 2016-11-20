# -*- coding: utf-8 -*-

'''
PySolvespace - PyQt 5 GUI with Solvespace Library
Copyright (C) 2016 Yuan Chang
E-mail: daan0014119@gmail.com
////Test program////
'''

import unittest
from core.test.testKernel import slvsKernel

def testChoose():
    print("Test Start")
    print("------")
    #Test python solvespace kernel
    suite = unittest.TestSuite()
    suite.addTest(slvsKernel('test_mutiLink'))
    #Test Qt
    unittest.main()
    print("------")
    print("Done.")

if __name__=="__main__":
    testChoose()
