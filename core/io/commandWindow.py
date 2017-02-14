# -*- coding: utf-8 -*-
from .modules import *
_translate = QCoreApplication.translate

class commandWindow(QDialog):
    def __init__(self, stack, parent=None):
        super(commandWindow, self).__init__(parent)
        self.undoView = QUndoView(stack)
        self.undoView.setEmptyLabel("Start Pyslvs")
        self.undoView.setAttribute(Qt.WA_QuitOnClose, False)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.undoView)
        self.setWindowTitle(_translate("MainWindow-UndoWindow", "Command List"))
        self.setSizeGripEnabled(False)
        size = QSize(250, 200)
        self.setMinimumSize(size)
        self.setMaximumSize(size)
        self.move(QPoint(QApplication.desktop().width()-self.width(), 60))
