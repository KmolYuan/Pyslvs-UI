# -*- coding: utf-8 -*-

"""The option dialog used to create or edit the point."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Union
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QDialog, QListWidgetItem, QColorDialog, QWidget
from qtpy.QtGui import QIcon, QPixmap
from pyslvs import VPoint, VLink, color_names
from pyslvs_ui.graphics import color_qt, color_icon
from .utility import set_custom_color, add_custom_color
from .relocate_point import RelocateDialog
from .edit_point_ui import Ui_Dialog


class EditPointDialog(QDialog, Ui_Dialog):
    """Option dialog."""

    def __init__(
        self,
        vpoints: List[VPoint],
        vlinks: List[VLink],
        pos: Union[int, bool],
        parent: QWidget
    ):
        """Input data reference from main window.

        + Needs VPoints and VLinks information.
        + If row is false: Create action.
        """
        super(EditPointDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        icon = self.windowIcon()
        self.icon = QIcon(QPixmap("icons:link.png"))
        self.vpoints = vpoints
        self.vlinks = vlinks
        vpoints_count = len(vpoints)
        for i, e in enumerate(color_names):
            self.color_box.insertItem(i, color_icon(e), e)
        for vlink in vlinks:
            self.no_selected.addItem(QListWidgetItem(self.icon, vlink.name))
        if pos is False:
            self.name_box.addItem(icon, f'Point{vpoints_count}')
            self.name_box.setEnabled(False)
            self.color_box.setCurrentIndex(self.color_box.findText('green'))
        else:
            for i in range(vpoints_count):
                self.name_box.insertItem(i, icon, f'Point{i}')
            self.name_box.setCurrentIndex(pos)
        self.type_box.currentIndexChanged.connect(self.__check_angle)
        self.__check_angle()

    def __link_item(self, name: str) -> QListWidgetItem:
        """Create a list item for a link."""
        return QListWidgetItem(self.icon, name)

    @Slot(int, name='on_name_box_currentIndexChanged')
    def __set_name(self, index: int) -> None:
        """Load the parameters of the point."""
        if not len(self.vpoints) > index:
            return
        vpoint = self.vpoints[index]
        self.x_box.setValue(vpoint.x)
        self.y_box.setValue(vpoint.y)
        set_custom_color(self.color_box, vpoint.color_str)
        self.type_box.setCurrentIndex(vpoint.type)
        self.angle_box.setValue(vpoint.angle)
        self.no_selected.clear()
        self.selected.clear()
        names = {vlink.name for vlink in self.vlinks}
        for name in vpoint.links:
            names.remove(name)
            self.selected.addItem(self.__link_item(name))
        for name in names:
            self.no_selected.addItem(self.__link_item(name))

    @Slot(int, name='on_color_box_currentIndexChanged')
    def __set_color(self, _=None) -> None:
        """Change the color icon of pick button."""
        self.color_pick_btn.setIcon(self.color_box.itemIcon(
            self.color_box.currentIndex()
        ))

    @Slot(name='on_color_pick_btn_clicked')
    def __set_rgb(self) -> None:
        """Add a custom color from current color."""
        color = QColorDialog.getColor(
            color_qt(self.color_box.currentText()),
            self
        )
        if color.isValid():
            add_custom_color(self.color_box, color)

    @Slot()
    def __check_angle(self) -> None:
        """Toggle the slider angle option."""
        enabled = self.type_box.currentIndex() != 0
        self.angle_label.setEnabled(enabled)
        self.angle_box.setEnabled(enabled)

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

    @Slot(name='on_relocate_option_clicked')
    def __relocate(self) -> None:
        """Relocate option."""
        dlg = RelocateDialog(self)
        dlg.show()
        if dlg.exec():
            self.x_box.setValue(dlg.get_x())
            self.y_box.setValue(dlg.get_y())
