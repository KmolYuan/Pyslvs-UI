# -*- coding: utf-8 -*-

"""The option dialog to specify target points."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Iterable, Iterator
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QWidget, QDialog, QListWidget, QListWidgetItem
from .targets_ui import Ui_Dialog


def list_texts(widget: QListWidget) -> Iterator[str]:
    """Generator to get the text from list widget."""
    for row in range(widget.count()):
        yield widget.item(row).text()


class TargetsDialog(QDialog, Ui_Dialog):
    """Option dialog.

    Select the targets from a group of options.
    """

    def __init__(
        self,
        description: str,
        prefix: str,
        not_target: Iterable[int],
        target: Iterable[int],
        parent: QWidget
    ):
        """Filter and show the target option (just like movable points)."""
        super(TargetsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.main_label.setText(description)
        self.prefix = prefix
        self.other_list.addItems(f"{self.prefix}{i}" for i in not_target)
        self.targets_list.addItems(f"{self.prefix}{i}" for i in target)

    @Slot(name='on_targets_add_clicked')
    @Slot(QListWidgetItem, name='on_other_list_itemDoubleClicked')
    def __add(self) -> None:
        """Add a new target joint."""
        row = self.other_list.currentRow()
        if not row > -1:
            return
        self.targets_list.addItem(self.other_list.takeItem(row))

    @Slot(name='on_other_add_clicked')
    @Slot(QListWidgetItem, name='on_targets_list_itemDoubleClicked')
    def __remove(self) -> None:
        """Remove a target joint."""
        row = self.targets_list.currentRow()
        if not row > -1:
            return
        self.other_list.addItem(self.targets_list.takeItem(row))

    def targets(self) -> List[int]:
        """Return a list of targets."""
        target_list = []
        for target in list_texts(self.targets_list):
            target_list.append(int(target[len(self.prefix):]))
        return target_list
