# -*- coding: utf-8 -*-

"""The option dialog use to create or edit the point."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List
from core.QtModules import (
    pyqtSlot,
    Qt,
    QDialog,
    QIcon,
    QPixmap,
    QListWidgetItem,
    QColorDialog,
    QWidget,
)
from core.graphics import (
    colorNames,
    colorQt,
    colorIcon,
)
from core.libs import VPoint, VLink
from .Ui_edit_point import Ui_Dialog


class EditPointDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the target path after closed.
    """
    
    def __init__(self,
        vpoints: List[VPoint],
        vlinks: List[VLink],
        pos: bool,
        parent: QWidget,
    ):
        """Input data reference from main window.
        
        + Needs VPoints and VLinks information.
        + If row is false: Create action.
        """
        super(EditPointDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = self.windowIcon()
        self.LinkIcon = QIcon(QPixmap(":/icons/link.png"))
        self.vpoints = vpoints
        self.vlinks = vlinks
        vpoints_count = len(vpoints)
        for i, e in enumerate(colorNames):
            self.color_box.insertItem(i, colorIcon(e), e)
        for vlink in vlinks:
            self.noSelected.addItem(QListWidgetItem(self.LinkIcon, vlink.name))
        if pos is False:
            self.name_box.addItem(icon, 'Point{}'.format(vpoints_count))
            self.name_box.setEnabled(False)
            self.color_box.setCurrentIndex(self.color_box.findText('Green'))
        else:
            for i in range(vpoints_count):
                self.name_box.insertItem(i, icon, 'Point{}'.format(i))
            self.name_box.setCurrentIndex(pos)
    
    @pyqtSlot(int)
    def on_name_box_currentIndexChanged(self, index):
        """Load the parameters of the point."""
        if not len(self.vpoints) > index:
            return
        vpoint = self.vpoints[index]
        self.x_box.setValue(vpoint.x)
        self.y_box.setValue(vpoint.y)
        colorText = vpoint.colorSTR
        colorIndex = self.color_box.findText(colorText)
        if colorIndex > -1:
            self.color_box.setCurrentIndex(colorIndex)
        else:
            self.color_box.addItem(colorIcon(colorText), colorText)
            self.color_box.setCurrentIndex(self.color_box.count() - 1)
        self.type_box.setCurrentIndex(vpoint.type)
        self.angle_box.setValue(vpoint.angle)
        self.noSelected.clear()
        self.selected.clear()
        for linkName in vpoint.links:
            self.selected.addItem(QListWidgetItem(self.LinkIcon, linkName))
        for vlink in self.vlinks:
            if vlink.name in vpoint.links:
                continue
            self.noSelected.addItem(QListWidgetItem(self.LinkIcon, vlink.name))
    
    @pyqtSlot(int)
    def on_color_box_currentIndexChanged(self, index):
        """Change the color icon of pick button."""
        self.colorpick_button.setIcon(self.color_box.itemIcon(
            self.color_box.currentIndex()
        ))
    
    @pyqtSlot()
    def on_colorpick_button_clicked(self):
        """Add a custom color from current color."""
        color = QColorDialog.getColor(
            colorQt(self.color_box.currentText()),
            self
        )
        if not color.isValid():
            return
        rgb_str = str((color.red(), color.green(), color.blue()))
        self.color_box.addItem(colorIcon(rgb_str), rgb_str)
        self.color_box.setCurrentIndex(self.color_box.count() - 1)
    
    @pyqtSlot(int)
    def on_type_box_currentIndexChanged(self, index):
        """Toggle the slider angle option."""
        self.angle_box.setEnabled(index != 0)
    
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
