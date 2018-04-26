# -*- coding: utf-8 -*-

"""The option dialog use to create or edit the point."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List
from core.QtModules import (
    QDialog,
    Qt,
    QIcon,
    QPixmap,
    QListWidgetItem,
    pyqtSlot,
)
from core.graphics import colorName, colorIcons
from core.libs import VPoint, VLink
from .Ui_edit_point import Ui_Dialog


class EditPointDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the target path after closed.
    """
    
    def __init__(self,
        points: List[VPoint],
        links: List[VLink],
        pos: bool = False,
        parent=None
    ):
        super(EditPointDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = self.windowIcon()
        self.LinkIcon = QIcon(QPixmap(":/icons/link.png"))
        self.points = points
        self.links = links
        for i, e in enumerate(colorName):
            self.Color.insertItem(i, colorIcons(e), e)
        for vlink in links:
            self.noSelected.addItem(QListWidgetItem(self.LinkIcon, vlink.name))
        if pos is False:
            self.Point.addItem(icon, 'Point{}'.format(len(points)))
            self.Point.setEnabled(False)
            self.Color.setCurrentIndex(self.Color.findText('Green'))
        else:
            for i in range(len(points)):
                self.Point.insertItem(i, icon, 'Point{}'.format(i))
            self.Point.setCurrentIndex(pos)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index):
        """Load the parameters of the point."""
        if not len(self.points) > index:
            return
        vpoint = self.points[index]
        self.X_coordinate.setValue(vpoint.x)
        self.Y_coordinate.setValue(vpoint.y)
        self.Color.setCurrentIndex(self.Color.findText(vpoint.colorSTR))
        self.Type.setCurrentIndex(vpoint.type)
        self.Angle.setValue(vpoint.angle)
        self.noSelected.clear()
        self.selected.clear()
        for linkName in vpoint.links:
            self.selected.addItem(QListWidgetItem(self.LinkIcon, linkName))
        for vlink in self.links:
            if vlink.name in vpoint.links:
                continue
            self.noSelected.addItem(QListWidgetItem(self.LinkIcon, vlink.name))
    
    @pyqtSlot(int)
    def on_Type_currentIndexChanged(self, index):
        """Toggle the slider angle option."""
        self.Angle.setEnabled(index!=0)
    
    @pyqtSlot(QListWidgetItem)
    def on_noSelected_itemDoubleClicked(self, item):
        """Add item to selected list."""
        self.selected.addItem(
            self.noSelected.takeItem(self.noSelected.row(item))
        )
    
    @pyqtSlot(QListWidgetItem)
    def on_selected_itemDoubleClicked(self, item):
        """Add item to no selected list."""
        self.noSelected.addItem(
            self.selected.takeItem(self.selected.row(item))
        )
