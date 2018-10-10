# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""
from PyQt5.QtCore import QPoint

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Optional
from abc import abstractmethod
from core.QtModules import (
    pyqtSlot,
    QApplication,
    QListWidgetItem,
    QInputDialog,
    QMessageBox,
    QAbcMeta,
)
from core.io import (
    AddStorage,
    DeleteStorage,
    AddStorageName,
    ClearStorageName,
)
from core.libs import parse_params
from .solver import SolverMethodInterface


class StorageMethodInterface(SolverMethodInterface, metaclass=QAbcMeta):

    """Abstract class for storage methods."""

    def __init__(self):
        super(StorageMethodInterface, self).__init__()

    def __add_storage(self, name: str, expr: str):
        """Add storage data function."""
        self.CommandStack.beginMacro(f"Add {{Mechanism: {name}}}")
        self.CommandStack.push(AddStorage(
            name,
            self.mechanism_storage,
            expr
        ))
        self.CommandStack.endMacro()

    @pyqtSlot(name='on_mechanism_storage_add_clicked')
    def addStorage(self):
        name = (
            self.mechanism_storage_name_tag.text() or
            self.mechanism_storage_name_tag.placeholderText()
        )
        self.CommandStack.beginMacro(f"Add {{Mechanism: {name}}}")
        exprs = ", ".join(vpoint.expr for vpoint in self.EntitiesPoint.data())
        self.__add_storage(name, f"M[{exprs}]")
        self.CommandStack.push(ClearStorageName(self.mechanism_storage_name_tag))
        self.CommandStack.endMacro()

    @pyqtSlot(name='on_mechanism_storage_copy_clicked')
    def copyStorage(self):
        """Copy the expression from a storage data."""
        item = self.mechanism_storage.currentItem()
        if item:
            QApplication.clipboard().setText(item.expr)

    @pyqtSlot(name='on_mechanism_storage_paste_clicked')
    def pasteStorage(self):
        """Add the storage data from string."""
        expr, ok = QInputDialog.getMultiLineText(
            self,
            "Storage",
            "Please input expression:"
        )
        if not ok:
            return
        try:
            # Put the expression into parser to see if it is legal.
            parse_params(expr)
        except Exception as e:
            print(e)
            QMessageBox.warning(
                self,
                "Loading failed",
                "Your expression is in an incorrect format."
            )
            return
        name, ok = QInputDialog.getText(
            self,
            "Storage",
            "Please input name tag:"
        )
        if not ok:
            return
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

    @pyqtSlot(name='on_mechanism_storage_delete_clicked')
    def deleteStorage(self):
        """Delete the storage data."""
        row = self.mechanism_storage.currentRow()
        if not row > -1:
            return
        name = self.mechanism_storage.item(row).text()
        self.CommandStack.beginMacro(f"Delete {{Mechanism: {name}}}")
        self.CommandStack.push(DeleteStorage(row, self.mechanism_storage))
        self.CommandStack.endMacro()

    @pyqtSlot(name='on_mechanism_storage_restore_clicked')
    def restoreStorage(self, item: Optional[QListWidgetItem] = None):
        """Restore the storage data."""
        if item is None:
            item = self.mechanism_storage.currentItem()
        if not item:
            return
        reply = QMessageBox.question(
            self,
            "Storage",
            "Restore mechanism will overwrite the canvas.\n"
            "Do you want to continue?"
        )
        if reply != QMessageBox.Yes:
            return
        name = item.text()
        self.CommandStack.beginMacro(f"Restore from {{Mechanism: {name}}}")

        # After saved storage, clean all the item of two table widgets.
        self.EntitiesPoint.clear()
        self.EntitiesLink.clear()
        self.InputsWidget.variableExcluding()

        self.parseExpression(item.expr)
        self.CommandStack.push(DeleteStorage(
            self.mechanism_storage.row(item),
            self.mechanism_storage
        ))
        self.CommandStack.push(AddStorageName(name, self.mechanism_storage_name_tag))
        self.CommandStack.endMacro()

    def getStorage(self) -> Tuple[Tuple[str, str], ...]:
        """Get storage data."""
        return tuple((
            self.mechanism_storage.item(row).text(),
            self.mechanism_storage.item(row).expr
        ) for row in range(self.mechanism_storage.count()))

    def addMultipleStorage(self, exprs: Tuple[Tuple[str, str], ...]):
        """Add storage data from database."""
        for name, expr in exprs:
            self.__add_storage(name, expr)

    @abstractmethod
    def commandReload(self, index: int) -> None:
        ...

    @abstractmethod
    def addTargetPoint(self) -> None:
        ...

    @abstractmethod
    def setMousePos(self, x: float, y: float) -> None:
        ...

    @abstractmethod
    def commit(self, is_branch: bool = False) -> None:
        ...

    @abstractmethod
    def commit_branch(self) -> None:
        ...

    @abstractmethod
    def enableMechanismActions(self) -> None:
        ...

    @abstractmethod
    def copyCoord(self) -> None:
        ...

    @abstractmethod
    def copyPointsTable(self) -> None:
        ...

    @abstractmethod
    def copyLinksTable(self) -> None:
        ...

    @abstractmethod
    def canvas_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def link_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def customizeZoom(self) -> None:
        ...

    @abstractmethod
    def resetOptions(self) -> None:
        ...
