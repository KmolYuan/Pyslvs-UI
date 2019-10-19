# -*- coding: utf-8 -*-

"""The option dialog use to create or edit the point."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Union
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QDialog, QListWidgetItem, QColorDialog, QWidget
from qtpy.QtGui import QIcon, QPixmap
from pyslvs import VPoint, VLink
from pyslvs_ui.graphics import color_names, color_qt, color_icon
from .edit_point_ui import Ui_Dialog


class EditPointDialog(QDialog, Ui_Dialog):

    """Option dialog.

    Only edit the target path after closed.
    """

    def __init__(
        self,
        vpoints: List[VPoint],
        vlinks: List[VLink],
        pos: Union[int, bool],
        parent: QWidget,
    ):
        """Input data reference from main window.

        + Needs VPoints and VLinks information.
        + If row is false: Create action.
        """
        super(EditPointDialog, self).__init__(parent)
        self.setupUi(self)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)
        icon = self.windowIcon()
        self.link_icon = QIcon(QPixmap(":/icons/link.png"))
        self.vpoints = vpoints
        self.vlinks = vlinks
        vpoints_count = len(vpoints)
        for i, e in enumerate(color_names):
            self.color_box.insertItem(i, color_icon(e), e)
        for vlink in vlinks:
            self.noSelected.addItem(QListWidgetItem(self.link_icon, vlink.name))
        if pos is False:
            self.name_box.addItem(icon, f'Point{vpoints_count}')
            self.name_box.setEnabled(False)
            self.color_box.setCurrentIndex(self.color_box.findText('Green'))
        else:
            for i in range(vpoints_count):
                self.name_box.insertItem(i, icon, f'Point{i}')
            self.name_box.setCurrentIndex(pos)

    @Slot(int, name='on_name_box_currentIndexChanged')
    def __set_name(self, index: int) -> None:
        """Load the parameters of the point."""
        if not len(self.vpoints) > index:
            return
        vpoint = self.vpoints[index]
        self.x_box.setValue(vpoint.x)
        self.y_box.setValue(vpoint.y)
        color_text = vpoint.color_str
        color_index = self.color_box.findText(color_text)
        if color_index > -1:
            self.color_box.setCurrentIndex(color_index)
        else:
            self.color_box.addItem(color_icon(color_text), color_text)
            self.color_box.setCurrentIndex(self.color_box.count() - 1)
        self.type_box.setCurrentIndex(vpoint.type)
        self.angle_box.setValue(vpoint.angle)
        self.noSelected.clear()
        self.selected.clear()
        for linkName in vpoint.links:
            self.selected.addItem(QListWidgetItem(self.link_icon, linkName))
        for vlink in self.vlinks:
            if vlink.name in vpoint.links:
                continue
            self.noSelected.addItem(QListWidgetItem(self.link_icon, vlink.name))

    @Slot(int, name='on_color_box_currentIndexChanged')
    def __set_color(self, _=None) -> None:
        """Change the color icon of pick button."""
        self.color_pick_button.setIcon(self.color_box.itemIcon(
            self.color_box.currentIndex()
        ))

    @Slot(name='on_color_pick_button_clicked')
    def __set_rgb(self) -> None:
        """Add a custom color from current color."""
        color = QColorDialog.getColor(
            color_qt(self.color_box.currentText()),
            self
        )
        if not color.isValid():
            return
        rgb_str = str((color.red(), color.green(), color.blue()))
        self.color_box.addItem(color_icon(rgb_str), rgb_str)
        self.color_box.setCurrentIndex(self.color_box.count() - 1)

    @Slot(int, name='on_type_box_currentIndexChanged')
    def __set_type(self, index: int) -> None:
        """Toggle the slider angle option."""
        self.angle_box.setEnabled(index != 0)

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
