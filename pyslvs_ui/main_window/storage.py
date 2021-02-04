# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, Dict, Mapping, Optional
from abc import ABC
from qtpy.QtCore import Slot
from qtpy.QtWidgets import (
    QApplication,
    QListWidgetItem,
    QInputDialog,
    QMessageBox,
)
from pyslvs import parse_params, VPoint
from pyslvs_ui.widgets import (
    AddStorage,
    DeleteStorage,
    AddStorageName,
    ClearStorageName,
)
from pyslvs_ui.info import logger
from .solver import SolverMethodInterface


class StorageMethodInterface(SolverMethodInterface, ABC):
    """Abstract class for storage methods."""

    def __add_storage(self, name: str, expr: str) -> None:
        """Add storage data function."""
        self.cmd_stack.push(AddStorage(
            name,
            self.mechanism_storage,
            expr
        ))

    @Slot(name='on_mechanism_storage_add_clicked')
    def __add_current_storage(self) -> None:
        name = (
            self.mechanism_storage_name_tag.text()
            or self.mechanism_storage_name_tag.placeholderText()
        )
        self.cmd_stack.beginMacro(f"Add {{Mechanism: {name}}}")
        self.__add_storage(name, self.get_expression())
        self.cmd_stack.push(ClearStorageName(self.mechanism_storage_name_tag))
        self.cmd_stack.endMacro()

    @Slot(name='on_mechanism_storage_copy_clicked')
    def __copy_storage(self) -> None:
        """Copy the expression from a storage data."""
        item = self.mechanism_storage.currentItem()
        if item:
            QApplication.clipboard().setText(item.expr)

    @Slot(name='on_mechanism_storage_paste_clicked')
    def __paste_storage(self) -> None:
        """Add the storage data from string."""
        expr, ok = QInputDialog.getMultiLineText(
            self,
            "Storage",
            "Please input expression:"
        )
        if not ok:
            return
        self.ask_add_storage(expr)

    def ask_add_storage(self, expr: str) -> bool:
        try:
            # Put the expression into parser to see if it is legal
            parse_params(expr)
        except Exception as error:
            logger.warn(error)
            QMessageBox.warning(
                self,
                "Loading failed",
                "Your expression is in an incorrect format."
            )
            return False
        name, ok = QInputDialog.getText(
            self,
            "Storage",
            "Please input name tag:"
        )
        if not ok:
            return False
        name_list = [
            self.mechanism_storage.item(i).text()
            for i in range(self.mechanism_storage.count())
        ]
        i = 0
        name = name or f"Prototype_{i}"
        while name in name_list:
            name = f"Prototype_{i}"
            i += 1
        self.__add_storage(name, expr)
        return True

    @Slot(name='on_mechanism_storage_delete_clicked')
    def __delete_storage(self) -> None:
        """Delete the storage data."""
        row = self.mechanism_storage.currentRow()
        if not row > -1:
            return
        self.cmd_stack.push(DeleteStorage(row, self.mechanism_storage))

    @Slot(name='on_mechanism_storage_restore_clicked')
    @Slot(QListWidgetItem, name='on_mechanism_storage_itemDoubleClicked')
    def __restore_storage(self, item: Optional[QListWidgetItem] = None) -> None:
        """Restore the storage data."""
        if item is None:
            item = self.mechanism_storage.currentItem()
        if not item:
            return

        if QMessageBox.question(
            self,
            "Storage",
            "Restore mechanism will overwrite the canvas.\n"
            "Do you want to continue?"
        ) != QMessageBox.Yes:
            return

        name = item.text()
        self.cmd_stack.beginMacro(f"Restore from {{Mechanism: {name}}}")

        # Clean all the item of two table widgets
        for i in range(self.entities_point.rowCount()):
            self.delete_point(0)
        for i in range(self.entities_link.rowCount() - 1):
            self.delete_link(1)

        self.parse_expression(item.expr)
        self.cmd_stack.push(DeleteStorage(
            self.mechanism_storage.row(item),
            self.mechanism_storage
        ))
        self.cmd_stack.push(AddStorageName(name, self.mechanism_storage_name_tag))
        self.cmd_stack.endMacro()
        self.main_canvas.zoom_to_fit()

    def get_storage(self) -> Mapping[str, str]:
        """Get storage data."""
        storage: Dict[str, str] = {}
        for row in range(self.mechanism_storage.count()):
            item: QListWidgetItem = self.mechanism_storage.item(row)
            storage[item.text()] = item.expr
        return storage

    def add_multiple_storage(self, exprs: Mapping[str, str]) -> None:
        """Add storage data from database."""
        for name, expr in exprs.items():
            self.__add_storage(name, expr)

    def get_expression(
        self,
        points: Optional[Sequence[VPoint]] = None,
        indent: int = -1
    ) -> str:
        """Get current mechanism expression."""
        if points is None:
            points = self.vpoint_list
        if not points:
            return "M[]"
        sep = ",\n" if indent > 0 else ", "
        head = "M["
        end = "]"
        if indent > 0:
            head += '\n'
            end = '\n' + end
        return head + sep.join(" " * indent + p.expr() for p in points) + end
