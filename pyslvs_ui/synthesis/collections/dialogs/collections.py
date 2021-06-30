# -*- coding: utf-8 -*-

"""The option dialog to load the structure data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from copy import deepcopy
from typing import Dict, Mapping, Callable, Any
from qtpy.QtCore import Qt, Slot
from qtpy.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QInputDialog,
    QMessageBox,
    QListWidgetItem,
    QWidget,
)
from pyslvs import collection_list, all_collections
from pyslvs_ui.graphics import PreviewCanvas
from .collections_ui import Ui_Dialog


class CollectionsDialog(QDialog, Ui_Dialog):
    """Option dialog.

    Load the settings after closed.
    Any add, rename, delete operations will be apply immediately
    """
    collections: Dict[str, Any]
    params: Mapping[str, Any]

    def __init__(
        self,
        collections: Mapping[str, Any],
        get_collection: Callable[[], Mapping[str, Any]],
        project_no_save: Callable[[], None],
        show_ticks: int,
        monochrome: bool,
        parent: QWidget
    ):
        """We put the 'collections' (from iteration widget) reference here."""
        super(CollectionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint
                            & ~Qt.WindowContextHelpButtonHint)
        self.collections = dict(collections)
        self.get_collection = get_collection
        self.project_no_save = project_no_save

        # Current profile name
        self.name = ""
        self.params = {}
        self.preview_canvas = PreviewCanvas(self)
        self.preview_layout.addWidget(self.preview_canvas)
        self.preview_canvas.set_show_ticks(show_ticks)
        self.preview_canvas.set_monochrome_mode(monochrome)
        self.common_list.addItems(all_collections())
        self.collections_list.addItems(self.collections)

        # Splitter
        self.main_splitter.setSizes([200, 200])
        self.sub_splitter.setSizes([100, 200])

        self.__has_collection()
        self.__can_open()

    @Slot(str, name='on_collections_list_currentTextChanged')
    def __can_open(self, _=None) -> None:
        """Set the button box to enable when data is already."""
        self.btn_box.button(QDialogButtonBox.Open).setEnabled(
            self.collections_list.currentRow() > -1
        )

    def __has_collection(self) -> None:
        """Set the buttons to enable when user choose a data."""
        has_collection = bool(self.collections)
        for button in [
            self.rename_btn,
            self.copy_btn,
            self.delete_btn
        ]:
            button.setEnabled(has_collection)

    @Slot(name='on_rename_btn_clicked')
    def __rename(self) -> None:
        """Show up a string input to change the data name."""
        row = self.collections_list.currentRow()
        if not row > -1:
            return

        name, ok = QInputDialog.getText(
            self,
            "Profile name",
            "Please enter the profile name:"
        )
        if not ok:
            return

        if not name:
            QMessageBox.warning(
                self,
                "Profile name",
                "Can not use blank string to rename."
            )
            return

        item = self.collections_list.item(row)
        self.collections[name] = self.collections.pop(item.text())
        item.setText(name)
        self.project_no_save()

    @Slot(name='on_copy_btn_clicked')
    def __copy(self) -> None:
        """Ask a name to copy a data."""
        row = self.collections_list.currentRow()
        if not row > -1:
            return

        name, ok = QInputDialog.getText(
            self,
            "Profile name",
            "Please enter a new profile name:"
        )
        if not ok:
            return

        if not name:
            QMessageBox.warning(
                self,
                "Profile name",
                "Can not use blank string to rename."
            )
            return

        name_old = self.collections_list.item(row).text()
        self.collections[name] = self.collections[name_old].copy()
        self.collections_list.addItem(name)
        self.project_no_save()

    @Slot(name='on_delete_btn_clicked')
    def __delete(self) -> None:
        """Delete a data."""
        row = self.collections_list.currentRow()
        if not row > -1:
            return

        if QMessageBox.question(
            self,
            "Delete",
            "Do you want to delete this structure?"
        ) != QMessageBox.Yes:
            return

        item = self.collections_list.takeItem(row)
        self.collections.pop(item.text())
        self.preview_canvas.clear()
        self.__has_collection()
        self.project_no_save()

    @Slot(QListWidgetItem, name='on_common_list_itemClicked')
    def __choose_common(self, _=None) -> None:
        """Update preview canvas for common data."""
        item = self.common_list.currentItem()
        if not item:
            return

        self.name = item.text()
        self.params = collection_list(self.name)
        self.preview_canvas.from_profile(self.params)

    @Slot(QListWidgetItem, name='on_collections_list_itemClicked')
    def __choose_collections(self, _=None) -> None:
        """Update preview canvas for a project data."""
        item = self.collections_list.currentItem()
        if not item:
            return

        self.name = item.text()
        self.params = deepcopy(self.collections[self.name])
        self.preview_canvas.from_profile(self.params)

    @Slot(name='on_project_btn_clicked')
    def __from_canvas(self) -> None:
        """Get a collection data from current mechanism."""
        try:
            collection = self.get_collection()
        except ValueError as error:
            QMessageBox.warning(self, "Mechanism not support.", str(error))
            return

        num = 0
        name = f"mechanism{num}"
        while name in self.collections:
            name = f"mechanism{num}"
            num += 1
        self.collections[name] = deepcopy(collection)
        self.collections_list.addItem(name)
        self.project_no_save()
        self.__has_collection()

    @Slot(name='on_common_load_clicked')
    @Slot(QListWidgetItem, name='on_common_list_itemDoubleClicked')
    def __load_common(self, _=None) -> None:
        """Load a common data and close."""
        self.__choose_common()
        self.accept()

    @Slot(name='on_btn_box_accepted')
    @Slot(QListWidgetItem, name='on_collections_list_itemDoubleClicked')
    def __load_collections(self, _=None) -> None:
        """Load a project data and close."""
        self.__choose_collections()
        self.accept()
