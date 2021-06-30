# -*- coding: utf-8 -*-

"""The option dialog to set the custom points and the multiple joints."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QDialog
from .customs_ui import Ui_Dialog

if TYPE_CHECKING:
    from pyslvs_ui.synthesis import ConfigureWidget


class CustomsDialog(QDialog, Ui_Dialog):
    """Option dialog.

    name: str = 'P1', 'P2', ...
    num: int = 1, 2, ...

    Settings will be edited in each operation.
    """

    def __init__(self, parent: ConfigureWidget):
        """Add data and widget references from the parent."""
        super(CustomsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        canvas = parent.configure_canvas
        self.cus = canvas.cus
        self.same = canvas.same
        self.pos = canvas.pos
        self.status = canvas.status
        self.joint_combobox = parent.joint_name
        for row in range(parent.grounded_list.count()):
            self.link_choose.addItem(parent.grounded_list.item(row).text())
        for name, link in self.cus.items():
            self.custom_list.addItem(f"P{name} -> {link}")
        self.__reload_quote_choose()
        self.quote_choose.setCurrentIndex(0)
        for s, qs in self.same.items():
            self.multiple_list.addItem(f"P{s} -> P{qs}")

    def __reload_quote_choose(self) -> None:
        """Reload joints from 'pos' dict."""
        s_old = self.quote_choose.currentText()
        self.quote_choose.clear()
        for i in self.pos:
            if i not in self.same:
                self.quote_choose.addItem(f'P{i}')
        self.quote_choose.setCurrentIndex(self.quote_choose.findText(s_old))

    @Slot(name='on_add_btn_clicked')
    def __add_cus(self) -> None:
        """Add a custom point by dependents."""
        row = self.link_choose.currentIndex()
        if not row > -1:
            return

        try:
            new_num = max(self.cus)
        except ValueError:
            new_num = max(self.pos)
        new_num += 1
        new_name = f"P{new_num}"
        self.cus[new_num] = row
        self.pos[new_num] = (0., 0.)
        self.status[new_num] = False
        self.custom_list.addItem(f"{new_name} -> {self.link_choose.itemText(row)}")
        self.joint_combobox.addItem(new_name)

    @Slot(name='on_delete_btn_clicked')
    def __delete_cus(self) -> None:
        """Remove a custom point."""
        row = self.custom_list.currentRow()
        if not row > -1:
            return

        name = self.custom_list.item(row).text().split(" -> ")[0]
        num = int(name.replace('P', ''))
        self.cus.pop(num)
        self.pos.pop(num)
        self.status.pop(num)
        self.custom_list.takeItem(row)
        self.joint_combobox.removeItem(num)

    @Slot(str, name='on_quote_choose_currentIndexChanged')
    def __set_quote(self, s: str) -> None:
        """Update the joint symbols when switch quote."""
        self.quote_link_choose.clear()
        if not s:
            return

        for row in range(self.link_choose.count()):
            link_text = self.link_choose.itemText(row)
            if s in link_text.replace('(', '').replace(')', '').split(", "):
                self.quote_link_choose.addItem(link_text)

    @Slot(str, name='on_quote_link_choose_currentIndexChanged')
    def __set_quote_link(self, s: str) -> None:
        """Update the joint symbols when switch quote link."""
        self.joint_choose.clear()
        if not s:
            return

        for joint in s.replace('(', '').replace(')', '').split(", "):
            if joint == self.quote_choose.currentText():
                continue
            if int(joint.replace('P', '')) in self.same:
                continue
            self.joint_choose.addItem(joint)

    @Slot(name='on_add_mj_btn_clicked')
    def __add_multi_joint(self) -> None:
        """Add a multiple joint by dependents."""
        s = self.joint_choose.currentText()
        if not s:
            return

        joint = int(s.replace('P', ''))
        qs = self.quote_choose.currentText()
        self.same[joint] = int(qs.replace('P', ''))
        self.multiple_list.addItem(f"{s} -> {qs}")
        self.__reload_quote_choose()

    @Slot(name='on_delete_mj_btn_clicked')
    def __delete_multi_joint(self) -> None:
        """Remove a multiple joint."""
        row = self.multiple_list.currentRow()
        if not row > -1:
            return

        name = self.multiple_list.item(row).text().split(" -> ")[0]
        joint = int(name.replace('P', ''))
        self.same.pop(joint)
        self.multiple_list.takeItem(row)
        self.__reload_quote_choose()
