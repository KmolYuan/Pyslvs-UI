# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple
from core.QtModules import (
    QApplication,
    QListWidgetItem,
    QInputDialog,
    QMessageBox,
)
from core.io import (
    AddStorage,
    DeleteStorage,
    AddStorageName,
    ClearStorageName,
)
from core.libs import parse_params


def _addStorage(self, name: str, expr: str):
    """Add storage data function."""
    self.CommandStack.beginMacro("Add {{Mechanism: {}}}".format(name))
    self.CommandStack.push(AddStorage(
        name,
        self.mechanism_storage,
        expr
    ))
    self.CommandStack.endMacro()


def addStorage(self):
    name = (
        self.mechanism_storage_name_tag.text() or
        self.mechanism_storage_name_tag.placeholderText()
    )
    self.CommandStack.beginMacro("Add {{Mechanism: {}}}".format(name))
    _addStorage(self, name, "M[{}]".format(", ".join(
        vpoint.expr for vpoint in self.EntitiesPoint.data()
    )))
    self.CommandStack.push(ClearStorageName(self.mechanism_storage_name_tag))
    self.CommandStack.endMacro()


def copyStorage(self):
    """Copy the expression from a storage data."""
    item = self.mechanism_storage.currentItem()
    if item:
        QApplication.clipboard().setText(item.expr)


def pasteStorage(self):
    """Add the storage data from string."""
    expr, ok = QInputDialog.getMultiLineText(self,
        "Storage",
        "Please input expression:"
    )
    if not ok:
        return
    try:
        #Put the expression into parser to see if it is legal.
        parse_params(expr)
    except:
        QMessageBox.warning(self,
            "Loading failed",
            "Your expression is in an incorrect format."
        )
        return
    name, ok = QInputDialog.getText(self,
        "Storage",
        "Please input name tag:"
    )
    if not ok:
        return
    if not name:
        nameList = [
            self.mechanism_storage.item(i).text()
            for i in range(self.mechanism_storage.count())
        ]
        i = 0
        while "Prototype_{}".format(i) in nameList:
            i += 1
        name = "Prototype_{}".format(i)
    _addStorage(self, name, expr)


def deleteStorage(self):
    """Delete the storage data."""
    row = self.mechanism_storage.currentRow()
    if not row>-1:
        return
    self.CommandStack.beginMacro("Delete {{Mechanism: {}}}".format(
        self.mechanism_storage.item(row).text()
    ))
    self.CommandStack.push(DeleteStorage(row, self.mechanism_storage))
    self.CommandStack.endMacro()


def restoreStorage(self, item: QListWidgetItem = None):
    """Restore the storage data."""
    if item is None:
        item = self.mechanism_storage.currentItem()
    if not item:
        return
    reply = QMessageBox.question(self,
        "Storage",
        "Restore mechanism will overwrite the canvas." +
        "\nDo you want to continue?"
    )
    if reply != QMessageBox.Yes:
        return
    name = item.text()
    self.CommandStack.beginMacro("Restore from {{Mechanism: {}}}".format(name))
    
    #After saved storage, clean all the item of two table widgets.
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


def getStorage(self) -> Tuple[Tuple[str, str]]:
    """Get storage data."""
    return tuple((
        self.mechanism_storage.item(row).text(),
        self.mechanism_storage.item(row).expr
    ) for row in range(self.mechanism_storage.count()))


def addStorages(self, exprs: Tuple[Tuple[str, str]]):
    """Add storage data from database."""
    for name, expr in exprs:
        _addStorage(self, name, expr)
