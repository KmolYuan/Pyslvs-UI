# -*- coding: utf-8 -*-

"""The option dialog to specify target points."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    Iterator,
    Optional,
)
from core.QtModules import (
    pyqtSlot,
    Qt,
    QDialog,
    QListWidget,
    QWidget,
)
from .Ui_targets import Ui_Dialog


def list_texts(
    widget: QListWidget,
    returnRow: bool = False
) -> Iterator[Tuple[Optional[int], str]]:
    """Generator to get the text from list widget."""
    for row in range(widget.count()):
        if returnRow:
            yield row, widget.item(row).text()
        else:
            yield widget.item(row).text()


class TargetsDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the settings after closed.
    """
    
    def __init__(self, parent: QWidget):
        """Filter and show the target option (just like moveable points)."""
        super(TargetsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        currentItem = parent.grounded_list.currentItem()
        
        if currentItem:
            
            def combo_texts(widget) -> Iterator[str]:
                """Generator to get the text from combobox widget."""
                for row in range(widget.count()):
                    yield widget.itemText(row)
            
            for text in combo_texts(parent.joint_name):
                if not parent.PreviewWindow.isMultiple(text) and (text not in (
                    currentItem.text()
                    .replace('(', '')
                    .replace(')', '')
                    .split(", ")
                )):
                    self.other_list.addItem(text)
        
        target_list = [text for text in list_texts(parent.target_list)]
        for row, text in list_texts(self.other_list, True):
            if text in target_list:
                self.targets_list.addItem(self.other_list.takeItem(row))
    
    @pyqtSlot(name='on_targets_add_clicked')
    def __add(self):
        """Add a new target joint."""
        row = self.other_list.currentRow()
        if not row > -1:
            return
        self.targets_list.addItem(self.other_list.takeItem(row))
    
    @pyqtSlot(name='on_other_add_clicked')
    def __remove(self):
        """Remove a target joint."""
        row = self.targets_list.currentRow()
        if not row>-1:
            return
        self.other_list.addItem(self.targets_list.takeItem(row))
