# -*- coding: utf-8 -*-
from .__init__ import *

class edit_stay_chain_show(QDialog, edit_chain_Dialog):
    Another_chain = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_stay_chain_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Chain_currentIndexChanged(self, index): self.Another_chain.emit(index)
    
    @pyqtSlot(int, int, int, float, float, float)
    def change_feedback(self, Point1, Point2, Point3, p1_p2, p2_p3, p1_p3):
        self.Point1.setCurrentIndex(Point1)
        self.Point2.setCurrentIndex(Point2)
        self.Point3.setCurrentIndex(Point3)
        self.p1_p2.setPlaceholderText(str(p1_p2))
        self.p2_p3.setPlaceholderText(str(p2_p3))
        self.p1_p3.setPlaceholderText(str(p1_p3))
