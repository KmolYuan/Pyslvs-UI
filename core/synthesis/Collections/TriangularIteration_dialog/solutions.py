# -*- coding: utf-8 -*-

"""The option dialog to add a solution."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    Qt,
    QDialog,
    QPixmap,
    QDialogButtonBox,
    QWidget,
)
from .Ui_solutions import Ui_Dialog


class SolutionsDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    + PLAP: Must have a driving joint.
    + PLLP: Two known joints.
    
    Only edit the settings after closed.
    """
    
    def __init__(self, mode: str, parent: QWidget):
        """Show the requirements and preview picture on interface."""
        super(SolutionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("{} solution".format(mode))
        
        if mode == 'PLAP':
            self.main_label.setText(
                "Two known points A (Driver) and B, " +
                "with angle β and length L0 to find out the coordinate of point C."
            )
            for row in range(parent.driver_list.count()):
                self.point_A.addItem(parent.driver_list.item(row).text())
            self.point_B.setEnable(False)
        elif mode == 'PLLP':
            self.main_label.setText(
                "Two known points A and B, " +
                "with length L0 and L1 to find out the coordinate of point C."
            )
            self.graph_label.setPixmap(QPixmap(":/icons/preview/PLLP.png"))
        
        for node, status in parent.PreviewWindow.status.items():
            if not status:
                continue
            if node in parent.PreviewWindow.same:
                continue
            if mode=='PLLP':
                self.point_A.addItem('P{}'.format(node))
                self.point_B.addItem('P{}'.format(node))
        self.point_A.currentIndexChanged.connect(self.__isOk)
        self.point_B.currentIndexChanged.connect(self.__isOk)
        self.__isOk()
    
    def __isOk(self):
        """Make button box enable if the settings is already."""
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            (self.point_A.currentText() != self.point_B.currentText()) and
            bool(self.point_A.currentText()) and
            bool(self.point_B.currentText())
        )
