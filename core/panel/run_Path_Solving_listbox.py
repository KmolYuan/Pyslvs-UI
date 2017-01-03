# -*- coding: utf-8 -*-
from .modules import *

class Path_Solving_listbox_show(QDialog, PathSolvingListbox_Dialog):
    def __init__(self, parent=None):
        super(Path_Solving_listbox_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
