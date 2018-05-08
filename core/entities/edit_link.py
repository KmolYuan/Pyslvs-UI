# -*- coding: utf-8 -*-

"""The option dialog use to create or edit the link."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Optional
from core.QtModules import (
    pyqtSlot,
    Qt,
    QDialog,
    QIcon,
    QPixmap,
    QListWidgetItem,
    QDialogButtonBox,
    QColorDialog,
)
from core.graphics import (
    colorNames,
    colorQt,
    colorIcon,
)
from core.libs import VPoint, VLink
from .Ui_edit_link import Ui_Dialog


class EditLinkDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the target path after closed.
    """
    
    def __init__(self,
        points: List[VPoint],
        links: List[VLink],
        pos: bool,
        parent
    ):
        super(EditLinkDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.points = points
        self.links = links
        icon = self.windowIcon()
        self.PointIcon = QIcon(QPixmap(":/icons/bearing.png"))
        for i, e in enumerate(colorNames):
            self.color_box.insertItem(i, colorIcon(e), e)
        for i in range(len(self.points)):
            self.noSelected.addItem(
                QListWidgetItem(self.PointIcon, 'Point{}'.format(i))
            )
        if pos is False:
            self.name_box.addItem(icon, "New link")
            self.name_box.setEnabled(False)
            self.color_box.setCurrentIndex(self.color_box.findText('Blue'))
        else:
            for vlink in self.links:
                self.name_box.insertItem(i, icon, vlink.name)
            self.name_box.setCurrentIndex(pos)
        self.name_edit.textChanged.connect(self.__isOk)
        self.__isOk()
    
    @pyqtSlot(str)
    def __isOk(self, p0: Optional[str] = None):
        """Set button box enable if options are ok."""
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            self.__legalName(self.name_edit.text())
        )
    
    def __legalName(self, name: str) -> bool:
        """Return this name is usable or not."""
        if not name.isidentifier():
            return False
        for i, vlink in enumerate(self.links):
            if (i != self.name_box.currentIndex()) and (name == vlink.name):
                return False
        return True
    
    @pyqtSlot(int)
    def on_name_box_currentIndexChanged(self, index):
        """Load the parameters of the link."""
        if len(self.links) > index:
            vlink = self.links[index]
            self.name_edit.setText(vlink.name)
            colorText = vlink.colorSTR
            colorIndex = self.color_box.findText(colorText)
            if colorIndex > -1:
                self.color_box.setCurrentIndex(colorIndex)
            else:
                self.color_box.addItem(colorIcon(colorText), colorText)
                self.color_box.setCurrentIndex(self.color_box.count() - 1)
            self.noSelected.clear()
            self.selected.clear()
            for point in vlink.points:
                self.selected.addItem(
                    QListWidgetItem(self.PointIcon, 'Point{}'.format(point))
                )
            for point in range(len(self.points)):
                if point in vlink.points:
                    continue
                self.noSelected.addItem(
                    QListWidgetItem(self.PointIcon, 'Point{}'.format(point))
                )
        not_grounded = index > 0
        for widget in (self.name_edit, self.color_box, self.colorpick_button):
            self.name_edit.setEnabled(not_grounded)
    
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
