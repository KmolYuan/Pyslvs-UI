# -*- coding: utf-8 -*-

import unittest
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class mainProject(unittest.TestCase):
    def setUp(self):
        self.args = 45
    
    def tearDown(self):
        del self.args
    
    def test_input(self):
        """"""
