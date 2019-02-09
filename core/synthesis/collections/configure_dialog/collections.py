# -*- coding: utf-8 -*-

"""The option dialog to load the structure data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from copy import deepcopy
from typing import (
    Dict,
    Callable,
    Any,
)
from core.QtModules import (
    Qt,
    QDialog,
    QDialogButtonBox,
    Slot,
    QInputDialog,
    QMessageBox,
    QListWidgetItem,
    QWidget,
)
from core.graphics import PreviewCanvas
from .Ui_collections import Ui_Dialog


_examples = {
    "Four bar linkage mechanism": {
        'Expression':
            "M["
            "J[R, P[-70, -70], L[ground, L1]],"
            "J[R, P[70, -70], L[ground, L2]],"
            "J[R, P[-70, 12.5], L[L1, L3]],"
            "J[R, P[70, 12.5], L[L2, L3]],"
            "J[R, P[0, 63.5], L[L3]]"
            "]",
        'input': [(0, 2)],
        'Graph': ((0, 1), (0, 2), (1, 3), (2, 3)),
        'Placement': {0: None, 1: None},
        'Target': {4: None},
        'cus': {4: 3},
        'same': {},
    },

    "Eight bar linkage mechanism": {
        'Expression':
            "M["
            "J[R, P[30.5, 10.5], L[ground, L1]],"
            "J[R, P[-14.5, 10.5], L[ground, L4, L5]],"
            "J[R, P[81.5, 60.5], L[L1, L2, L3]],"
            "J[R, P[-31.5, 86.5], L[L2, L4]],"
            "J[R, P[41.5, -38.5], L[L3, L5, L7]],"
            "J[R, P[-85.5, 9.5], L[L4, L6]],"
            "J[R, P[-37.5, -48.5], L[L6, L7]],"
            "J[R, P[35.5, -107.5], L[L7]]"
            "]",
        'input': [(0, 3)],
        'Graph': (
            (0, 1),
            (0, 4),
            (0, 5),
            (1, 2),
            (1, 3),
            (2, 4),
            (3, 5),
            (3, 7),
            (4, 6),
            (6, 7),
        ),
        'Placement': {0: None, 1: None},
        'Target': {10: None},
        'cus': {10: 7},
        'same': {2: 1, 4: 3, 7: 6},
    },

    "Ball lifter linkage mechanism": {
        'Expression':
            "M["
            "J[R, P[36.5, -59.5], L[ground, L1]],"
            "J[R, P[10, -94.12], L[ground, L4]],"
            "J[R, P[-28.5, -93.5], L[ground, L6]],"
            "J[R, P[102.5, -43.5], L[ground, L7]],"
            "J[R, P[77.5, -74.5], L[ground, L9]],"
            "J[R, P[28.82, -22.35], L[L1, L2, L3]],"
            "J[R, P[-18.5, -44.5], L[L2, L4]],"
            "J[R, P[-75.5, -59.5], L[L2, L5]],"
            "J[R, P[56.5, 29.5], L[L3, L7]],"
            "J[R, P[68.5, 71.5], L[L8, L3]],"
            "J[R, P[-47.06, -28.24], L[L5, L6]],"
            "J[R, P[107.5, 42.5], L[L8, L9]],"
            "J[R, P[-109.41, -49.41], L[L5]],"
            "J[R, P[44.12, 107.65], L[L8]]"
            "]",
        'input': [(0, 5)],
        'Graph': (
            (0, 1),
            (0, 4),
            (0, 9),
            (0, 6),
            (0, 7),
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 8),
            (3, 7),
            (5, 6),
            (8, 9),
        ),
        'Placement': {0: None, 1: None, 2: None, 3: None, 4: None},
        'Target': {13: None, 14: None},
        'cus': {13: 5, 14: 8},
        'same': {6: 5},
    },
}


class CollectionsDialog(QDialog, Ui_Dialog):

    """Option dialog.

    Load the settings after closed.
    Any add, rename, delete operations will be apply immediately
    """

    def __init__(
        self,
        collections: Dict[str, Any],
        get_collection: Callable[[], Dict[str, Any]],
        parent: QWidget
    ):
        """We put the 'collections' (from iteration widget) reference here."""
        super(CollectionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
            self.windowFlags() &
            ~Qt.WindowContextHelpButtonHint |
            Qt.WindowMaximizeButtonHint
        )

        self.collections = collections
        self.get_collection = get_collection

        # Current profile name.
        self.__name_loaded = ""

        self.preview_canvas = PreviewCanvas(self)
        self.preview_layout.addWidget(self.preview_canvas)
        for name in self.collections:
            self.collections_list.addItem(name)

        # Splitter
        self.main_splitter.setSizes([200, 200])
        self.sub_splitter.setSizes([100, 200])

        self.__has_collection()
        self.__can_open()

    @Slot(str, name='on_collections_list_currentTextChanged')
    def __can_open(self, _=None):
        """Set the button box to enable when data is already."""
        self.button_box.button(QDialogButtonBox.Open).setEnabled(
            self.collections_list.currentRow() > -1
        )

    def __has_collection(self):
        """Set the buttons to enable when user choose a data."""
        has_collection = bool(self.collections)
        for button in [
            self.rename_button,
            self.copy_button,
            self.delete_button
        ]:
            button.setEnabled(has_collection)

    def name(self) -> str:
        return self.__name_loaded

    def params(self) -> Dict[str, Any]:
        return self.__mech_params

    @Slot(name='on_rename_button_clicked')
    def __rename(self):
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

    @Slot(name='on_copy_button_clicked')
    def __copy(self):
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

    @Slot(name='on_delete_button_clicked')
    def __delete(self):
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
        del self.collections[item.text()]
        self.preview_canvas.clear()
        self.__has_collection()

    @Slot(str, name='on_common_list_currentTextChanged')
    def __choose_common(self, _=None):
        """Update preview canvas for common data."""
        item = self.common_list.currentItem()
        if not item:
            return

        self.__name_loaded = item.text()
        self.__mech_params = deepcopy(_examples[self.__name_loaded])
        self.preview_canvas.from_profile(self.__mech_params)

    @Slot(str, name='on_collections_list_currentTextChanged')
    def __choose_collections(self, _=None):
        """Update preview canvas for a workbook data."""
        item = self.collections_list.currentItem()
        if not item:
            return

        self.__name_loaded = item.text()
        self.__mech_params = deepcopy(self.collections[self.__name_loaded])
        self.preview_canvas.from_profile(self.__mech_params)

    @Slot(name='on_workbook_button_clicked')
    def __from_canvas(self):
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
        self.collections[name] = collection.copy()
        self.collections_list.addItem(name)

    @Slot(name='on_common_load_clicked')
    @Slot(QListWidgetItem, name='on_common_list_itemDoubleClicked')
    def __load_common(self, _=None):
        """Load a common data and close."""
        self.__choose_common()
        self.accept()

    @Slot(name='on_button_box_accepted')
    @Slot(QListWidgetItem, name='on_collections_list_itemDoubleClicked')
    def __load_collections(self, _=None):
        """Load a workbook data and close."""
        self.__choose_collections()
        self.accept()
