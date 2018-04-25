# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple
from core.QtModules import (
    pyqtSlot,
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
    PMKS_parser,
)


class StorageFunc:
    
    """A class contain storage functions."""
    
    def __clearStorage(self):
        """After saved storage,
        clean all the item of two table widgets.
        """
        self.Entities_Point.clear()
        self.Entities_Link.clear()
        self.InputsWidget.variableExcluding()
    
    @pyqtSlot()
    def on_mechanism_storage_add_clicked(self):
        name = self.mechanism_storage_name_tag.text()
        if not name:
            name = self.mechanism_storage_name_tag.placeholderText()
        self.CommandStack.beginMacro("Add {{Mechanism: {}}}".format(name))
        self.__addStorage(name, "M[{}]".format(", ".join(
            vpoint.expr for vpoint in self.Entities_Point.data()
        )))
        self.CommandStack.push(ClearStorageName(
            self.mechanism_storage_name_tag
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_mechanism_storage_copy_clicked(self):
        """Copy the expression from a storage data."""
        item = self.mechanism_storage.currentItem()
        if item:
            QApplication.clipboard().setText(item.expr)
    
    @pyqtSlot()
    def on_mechanism_storage_paste_clicked(self):
        """Add the storage data from string."""
        expr, ok = QInputDialog.getText(self,
            "Storage",
            "Please input expression:"
        )
        if not ok:
            return
        try:
            #Put the expression into parser to see if it is legal.
            PMKS_parser.parse(expr)
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
        self.__addStorage(name, expr, clear=False)
    
    def __addStorage(self, name, expr, clear=True):
        """Add storage data function."""
        self.CommandStack.beginMacro("Add {{Mechanism: {}}}".format(name))
        if clear:
            self.__clearStorage()
        self.CommandStack.push(AddStorage(
            name,
            self.mechanism_storage,
            expr
        ))
        self.CommandStack.endMacro()
        i = 0
        exprs = []
        for i in range(self.mechanism_storage.count()):
            exprs.append(self.mechanism_storage.item(i).text())
        while "Prototype_{}".format(i) in exprs:
            i += 1
        self.mechanism_storage_name_tag.setPlaceholderText(
            "Prototype_{}".format(i)
        )
    
    @pyqtSlot()
    def on_mechanism_storage_delete_clicked(self):
        """Delete the storage data."""
        row = self.mechanism_storage.currentRow()
        if not row>-1:
            return
        self.CommandStack.beginMacro("Delete {{Mechanism: {}}}".format(
            self.mechanism_storage.item(row).text()
        ))
        self.CommandStack.push(DeleteStorage(row, self.mechanism_storage))
        self.CommandStack.endMacro()
    
    @pyqtSlot(QListWidgetItem)
    def on_mechanism_storage_itemDoubleClicked(self, item):
        """Restore the storage data as below."""
        self.on_mechanism_storage_restore_clicked(item)
    
    @pyqtSlot()
    def on_mechanism_storage_restore_clicked(self, item=None):
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
        self.CommandStack.beginMacro(
            "Restore from {{Mechanism: {}}}".format(name)
        )
        self.__clearStorage()
        self.parseExpression(item.expr)
        self.CommandStack.push(DeleteStorage(
            self.mechanism_storage.row(item),
            self.mechanism_storage
        ))
        self.CommandStack.push(AddStorageName(
            name,
            self.mechanism_storage_name_tag
        ))
        self.CommandStack.endMacro()
    
    def loadStorage(self, exprs: Tuple[Tuple[str, str]]):
        """Load storage data from database."""
        for name, expr in exprs:
            self.__addStorage(name, expr, clear=False)
