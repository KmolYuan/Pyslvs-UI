# -*- coding: utf-8 -*-

"""The option dialog to specify target points."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    TYPE_CHECKING,
    Tuple,
    Iterator,
    Optional,
)
from core.QtModules import (
    Slot,
    Qt,
    QDialog,
    QListWidget,
    QListWidgetItem,
)
from .Ui_targets import Ui_Dialog

if TYPE_CHECKING:
    from core.synthesis.collections import ConfigureWidget


def list_texts(widget: QListWidget) -> Iterator[str]:
    """Generator to get the text from list widget."""
    for row in range(widget.count()):
        yield widget.item(row).text()


class TargetsDialog(QDialog, Ui_Dialog):

    """Option dialog.

    Only edit the settings after closed.
    """

    def __init__(self, parent: ConfigureWidget):
        """Filter and show the target option (just like movable points)."""
        super(TargetsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        canvas = parent.configure_canvas
        self.other_list.addItems(f"P{i}" for i in set(canvas.pos) - canvas.target)
        self.targets_list.addItems(f"P{i}" for i in canvas.target)

    @Slot(name='on_targets_add_clicked')
    @Slot(QListWidgetItem, name='on_other_list_itemDoubleClicked')
    def __add(self):
        """Add a new target joint."""
        row = self.other_list.currentRow()
        if not row > -1:
            return
        self.targets_list.addItem(self.other_list.takeItem(row))

    @Slot(name='on_other_add_clicked')
    @Slot(QListWidgetItem, name='on_targets_list_itemDoubleClicked')
    def __remove(self):
        """Remove a target joint."""
        row = self.targets_list.currentRow()
        if not row > -1:
            return
        self.other_list.addItem(self.targets_list.takeItem(row))
