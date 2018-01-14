# -*- coding: utf-8 -*-

from core.QtModules import *
from .Ui_TriangularIteration import Ui_Form

class CollectionTriangularIteration(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(CollectionTriangularIteration, self).__init__(parent)
        self.setupUi(self)
