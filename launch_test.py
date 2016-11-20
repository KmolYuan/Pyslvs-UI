# -*- coding: utf-8 -*-

'''
PySolvespace - PyQt 5 GUI with Solvespace Library
Copyright (C) 2016 Yuan Chang
E-mail: daan0014119@gmail.com
////Test program////
'''

import unittest
from core.test.testKernel import slvsKernel
from core.test.testQt import mainProject

def testChoose():
    print("Test Start")
    print("------")
    #Test python solvespace kernel
    unittest.TestLoader().loadTestsFromTestCase(slvsKernel)
    #Test Qt
    unittest.TestLoader().loadTestsFromTestCase(mainProject)
    #Start
    unittest.main()
    print("------")
    print("Done.")

if __name__=="__main__":
    testChoose()
