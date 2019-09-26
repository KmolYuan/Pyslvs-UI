# -*- coding: utf-8 -*-

"""The option dialog use to create or edit the link."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from re import match
from typing import List, Union
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import (
    QDialog,
    QListWidgetItem,
    QDialogButtonBox,
    QColorDialog,
    QWidget,
)
from qtpy.QtGui import QIcon, QPixmap
from pyslvs import VPoint, VLink
from pyslvs_ui.graphics import color_names, color_qt, color_icon
from .edit_link_ui import Ui_Dialog


class EditLinkDialog(QDialog, Ui_Dialog):

    """Option dialog.

    Only edit the target path after closed.
    """

    def __init__(
        self,
        vpoints: List[VPoint],
        vlinks: List[VLink],
        row: Union[int, bool],
        parent: QWidget
    ):
        """Input data reference from main window.

        + Needs VPoints and VLinks information.
        + If row is false: Create action.
        """
        super(EditLinkDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
            self.windowFlags()
            & ~Qt.WindowContextHelpButtonHint
        )
        self.vpoints = vpoints
        self.vlinks = vlinks
        icon = self.windowIcon()
        self.icon = QIcon(QPixmap(":/icons/bearing.png"))
        for i, e in enumerate(color_names):
            self.color_box.insertItem(i, color_icon(e), e)
        for i in range(len(self.vpoints)):
            self.noSelected.addItem(QListWidgetItem(self.icon, f'Point{i}'))
        if row is False:
            self.name_box.addItem(icon, "New link")
            self.name_box.setEnabled(False)
            self.color_box.setCurrentIndex(self.color_box.findText('Blue'))
        else:
            for i, vlink in enumerate(self.vlinks):
                self.name_box.insertItem(i, icon, vlink.name)
            self.name_box.setCurrentIndex(row)
        self.name_edit.textChanged.connect(self.__is_ok)
        self.__is_ok()

    @Slot()
    def __is_ok(self) -> None:
        """Set button box enable if options are ok."""
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(
            self.__legal_name(self.name_edit.text())
        )

    def __legal_name(self, name: str) -> bool:
        """Return this name is usable or not."""
        if not match("^[A-Za-z0-9_-]+$", name):
            return False
        for i, vlink in enumerate(self.vlinks):
            if i != self.name_box.currentIndex() and name == vlink.name:
                return False
        return True

    @Slot(int, name='on_name_box_currentIndexChanged')
    def __set_name(self, index: int) -> None:
        """Load the parameters of the link."""
        if not self.name_box.isEnabled():
            return
        if len(self.vlinks) > index:
            vlink = self.vlinks[index]
            self.name_edit.setText(vlink.name)
            color_text = vlink.color_str
            color_index = self.color_box.findText(color_text)
            if color_index > -1:
                self.color_box.setCurrentIndex(color_index)
            else:
                self.color_box.addItem(color_icon(color_text), color_text)
                self.color_box.setCurrentIndex(self.color_box.count() - 1)
            self.noSelected.clear()
            self.selected.clear()
            for p in vlink.points:
                self.selected.addItem(QListWidgetItem(self.icon, f'Point{p}'))
            for p in range(len(self.vpoints)):
                if p in vlink.points:
                    continue
                self.noSelected.addItem(QListWidgetItem(self.icon, f'Point{p}'))
        not_ground = index > 0
        for widget in (self.name_edit, self.color_box, self.color_pick_button):
            widget.setEnabled(not_ground)

    @Slot(int, name='on_color_box_currentIndexChanged')
    def __set_color(self, _=None) -> None:
        """Change the color icon of pick button."""
        self.color_pick_button.setIcon(self.color_box.itemIcon(
            self.color_box.currentIndex()
        ))

    @Slot(name='on_color_pick_button_clicked')
    def __set_rgb(self) -> None:
        """Add a custom color from current color."""
        color = color_qt(self.color_box.currentText())
        color = QColorDialog.getColor(color, self)
        if not color.isValid():
            return
        rgb_str = str((color.red(), color.green(), color.blue()))
        self.color_box.addItem(color_icon(rgb_str), rgb_str)
        self.color_box.setCurrentIndex(self.color_box.count() - 1)

    @Slot(QListWidgetItem, name='on_noSelected_itemDoubleClicked')
    def __add_selected(self, item: QListWidgetItem) -> None:
        """Add item to selected list."""
        self.selected.addItem(
            self.noSelected.takeItem(self.noSelected.row(item))
        )

    @Slot(QListWidgetItem, name='on_selected_itemDoubleClicked')
    def __add_no_selected(self, item: QListWidgetItem) -> None:
        """Add item to no selected list."""
        self.noSelected.addItem(
            self.selected.takeItem(self.selected.row(item))
        )
