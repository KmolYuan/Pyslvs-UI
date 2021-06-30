# -*- coding: utf-8 -*-

"""The option dialog used to create or edit the link."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from re import match
from typing import List, Union
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import (
    QDialog, QListWidgetItem, QDialogButtonBox, QColorDialog, QWidget,
)
from qtpy.QtGui import QIcon, QPixmap
from pyslvs import VPoint, VLink, color_names
from pyslvs_ui.graphics import color_qt, color_icon
from .utility import set_custom_color, add_custom_color
from .edit_link_ui import Ui_Dialog


class EditLinkDialog(QDialog, Ui_Dialog):
    """Option dialog."""

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
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.vpoints = vpoints
        self.vlinks = vlinks
        icon = self.windowIcon()
        self.icon = QIcon(QPixmap("icons:bearing.png"))
        for i, e in enumerate(color_names):
            self.color_box.insertItem(i, color_icon(e), e)
        for i in range(len(self.vpoints)):
            self.no_selected.addItem(QListWidgetItem(self.icon, f'Point{i}'))
        if row is False:
            names = {vlink.name for vlink in self.vlinks}
            n = 1
            name = f"link_{n}"
            while name in names:
                n += 1
                name = f"link_{n}"
            self.name_edit.setText(name)
            self.name_box.setEnabled(False)
            self.name_box.addItem(icon, "New link")
            self.color_box.setCurrentIndex(self.color_box.findText('blue'))
        else:
            for i, vlink in enumerate(self.vlinks):
                self.name_box.insertItem(i, icon, vlink.name)
            self.name_box.setCurrentIndex(row)
        self.name_edit.textChanged.connect(self.__is_ok)
        self.__is_ok()

    @Slot()
    def __is_ok(self) -> None:
        """Set button box enable if options are ok."""
        self.btn_box.button(QDialogButtonBox.Ok).setEnabled(
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

    def __point_item(self, p: int) -> QListWidgetItem:
        """Create a list item for a point."""
        return QListWidgetItem(self.icon, f'Point{p}')

    @Slot(int, name='on_name_box_currentIndexChanged')
    def __set_name(self, index: int) -> None:
        """Load the parameters of the link."""
        if not self.name_box.isEnabled():
            return
        if len(self.vlinks) > index:
            vlink = self.vlinks[index]
            self.name_edit.setText(vlink.name)
            set_custom_color(self.color_box, vlink.color_str)
            self.no_selected.clear()
            self.selected.clear()
            points = set(range(len(self.vpoints)))
            for p in vlink.points:
                points.remove(p)
                self.selected.addItem(self.__point_item(p))
            for p in points:
                self.no_selected.addItem(self.__point_item(p))
        not_ground = index > 0
        for widget in (self.name_edit, self.color_box, self.color_pick_btn):
            widget.setEnabled(not_ground)

    @Slot(int, name='on_color_box_currentIndexChanged')
    def __set_color(self, _=None) -> None:
        """Change the color icon of pick button."""
        self.color_pick_btn.setIcon(self.color_box.itemIcon(
            self.color_box.currentIndex()
        ))

    @Slot(name='on_color_pick_btn_clicked')
    def __set_rgb(self) -> None:
        """Add a custom color from current color."""
        color = color_qt(self.color_box.currentText())
        color = QColorDialog.getColor(color, self)
        if color.isValid():
            add_custom_color(self.color_box, color)

    @Slot(QListWidgetItem, name='on_no_selected_itemDoubleClicked')
    def __add_selected(self, item: QListWidgetItem) -> None:
        """Add item to selected list."""
        self.selected.addItem(
            self.no_selected.takeItem(self.no_selected.row(item))
        )

    @Slot(QListWidgetItem, name='on_selected_itemDoubleClicked')
    def __add_no_selected(self, item: QListWidgetItem) -> None:
        """Add item to no selected list."""
        self.no_selected.addItem(
            self.selected.takeItem(self.selected.row(item))
        )
