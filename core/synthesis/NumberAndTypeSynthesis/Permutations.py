# -*- coding: utf-8 -*-

from ...QtModules import *
from .Ui_Permutations import Ui_Form

class Permutations_show(QWidget, Ui_Form):
    def __init__(self, jointDataFunc, linkDataFunc, parent=None):
        super(Permutations_show, self).__init__(parent)
        self.setupUi(self)
        self.jointDataFunc = jointDataFunc
        self.linkDataFunc = linkDataFunc
    
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        self.Representation_text.setText("M[{}]".format(", ".join(str(vpoint) for vpoint in jointData)))
