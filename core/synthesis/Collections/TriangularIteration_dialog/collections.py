# -*- coding: utf-8 -*-

"""The option dialog to load the structure data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from copy import deepcopy
from typing import (
    Tuple,
    Dict,
    Callable,
    Any,
    Union,
    Optional,
)
from core.QtModules import (
    Qt,
    QDialog,
    QDialogButtonBox,
    pyqtSlot,
    QInputDialog,
    QMessageBox,
    QListWidgetItem,
    QWidget,
)
from core.graphics import PreviewCanvas
from .Ui_collections import Ui_Dialog


_mech_params_4Bar = {
    'Driver': {'P0': None},
    'Follower': {'P1': None},
    'Target': {'P4': None},
    'Link_expr': "ground[P0,P1];[P0,P2];[P1,P3];[P2,P3,P4]",
    'Expression': "PLAP[P0,L0,a0](P2);PLLP[P2,L1,L2,P1](P3);PLLP[P2,L3,L4,P3](P4)",
    'Graph': ((0, 1), (0, 2), (1, 3), (2, 3)),
    'constraint': [('P0', 'P1', 'P2', 'P3')],
    'pos': {
        0: (-70, -70),
        1: (70, -70),
        2: (-70, 12.5),
        3: (70, 12.5),
        4: (0, 63.5),
    },
    'cus': {'P4': 3},
    'same': {},
}

_mech_params_8Bar = {
    'Driver': {'P0': None},
    'Follower': {'P1': None},
    'Target': {'P10': None},
    'Link_expr': "ground[P0,P1];[P0,P3];[P3,P5];[P3,P6];[P1,P5,P8];" +
        "[P1,P6];[P8,P9];[P10,P6,P9]",
    'Expression': "PLAP[P0,L0,a0](P3);PLLP[P1,L1,L2,P3](P5);" +
        "PLLP[P3,L3,L4,P1](P6);PLLP[P1,L5,L6,P5](P8);PLLP[P6,L7,L8,P8](P9);" +
        "PLLP[P6,L9,L10,P9](P10)",
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
    'constraint': [('P0', 'P3', 'P5', 'P1')],
    'cus': {'P10': 7},
    'pos': {
        0: (30.5, 10.5),
        1: (-14.5, 10.5),
        2: (-18.5, 0.),
        3: (81.5, 60.5),
        4: (92.5, 75.5),
        5: (-31.5, 86.5),
        6: (41.5, -38.5),
        7: (19.5, -32.5),
        8: (-85.5, 9.5),
        9: (-37.5, -48.5),
        10: (35.5, -107.5),
    },
    'same': {2: 1, 4: 3, 7: 6},
}

_mech_params_BallLifter = {
    'Driver': {'P0': None},
    'Follower': {'P1': None, 'P2': None, 'P3': None, 'P4': None},
    'Target': {'P13': None, 'P14': None},
    'Link_expr': "ground[P0,P1,P2,P3,P4];[P0,P5];[P5,P7,P8];[P10,P5,P9];" +
        "[P1,P7];[P11,P13,P8];[P11,P2];[P3,P9];[P10,P12,P14];[P12,P4]",
    'Expression': "PLAP[P0,L0,a0](P5);PLLP[P1,L1,L2,P5](P7);" +
        "PLLP[P7,L3,L4,P5](P8);PLLP[P5,L5,L6,P3](P9);PLLP[P5,L7,L8,P9](P10);" +
        "PLLP[P8,L9,L10,P2](P11);PLLP[P4,L11,L12,P10](P12);" +
        "PLLP[P8,L13,L14,P11](P13);PLLP[P12,L15,L16,P10](P14)",
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
    'constraint': [('P0', 'P5', 'P9', 'P3'), ('P0', 'P5', 'P7', 'P1')],
    'cus': {'P13': 5, 'P14': 8},
    'pos': {
        0: (36.5, -59.5),
        1: (10.0, -94.12),
        2: (-28.5, -93.5),
        3: (102.5, -43.5),
        4: (77.5, -74.5),
        5: (28.82, -22.35),
        6: (23.5, 22.5),
        7: (-18.5, -44.5),
        8: (-75.5, -59.5),
        9: (56.5, 29.5),
        10: (68.5, 71.5),
        11: (-47.06, -28.24),
        12: (107.5, 42.5),
        13: (-109.41, -49.41),
        14: (44.12, 107.65),
    },
    'same': {6: 5},
}


class CollectionsDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Load the settings after closed.
    Any add, rename, delete opreations will be apply immediately
    """
    
    def __init__(self,
        collections: Dict[str, Any],
        getCollection: Callable[[], Dict[str, Any]],
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
        self.getCollection = getCollection
        
        #Current profile name.
        self.__name_loaded = ""
        
        def get_solutions_func() -> Tuple[str]:
            """Return solutions to preview canvas."""
            try:
                return self.collections[self.__name_loaded]['Expression']
            except KeyError:
                if self.__name_loaded == "Four bar linkage mechanism":
                    return _mech_params_4Bar['Expression']
                elif self.__name_loaded == "Eight bar linkage mechanism":
                    return _mech_params_8Bar['Expression']
                elif self.__name_loaded == "Ball lifter linkage mechanism":
                    return _mech_params_BallLifter['Expression']
                else:
                    return ()
        
        self.PreviewCanvas = PreviewCanvas(get_solutions_func, self)
        self.preview_layout.addWidget(self.PreviewCanvas)
        self.show_solutions.clicked.connect(self.PreviewCanvas.setShowSolutions)
        for name in self.collections:
            self.collections_list.addItem(name)
        
        #Splitter
        self.main_splitter.setSizes([200, 200])
        self.sub_splitter.setSizes([100, 200])
        
        #Signals
        self.common_list.currentTextChanged.connect(self.__chooseCommon)
        self.common_list.itemDoubleClicked.connect(self.__loadCommon)
        self.common_load.clicked.connect(self.__loadCommon)
        self.collections_list.currentTextChanged.connect(self.__chooseCollections)
        self.collections_list.currentTextChanged.connect(self.__canOpen)
        self.collections_list.itemDoubleClicked.connect(self.__loadCollections)
        self.buttonBox.accepted.connect(self.__loadCollections)
        self.__hasCollection()
        self.__canOpen()
    
    def __canOpen(self):
        """Set the button box to enable when data is already."""
        self.buttonBox.button(QDialogButtonBox.Open).setEnabled(
            self.collections_list.currentRow() > -1
        )
    
    def __hasCollection(self):
        """Set the buttons to enable when user choose a data."""
        hasCollection = bool(self.collections)
        for button in [
            self.rename_button,
            self.copy_button,
            self.delete_button
        ]:
            button.setEnabled(hasCollection)
    
    def name(self) -> str:
        return self.__name_loaded
    
    def params(self) -> Dict[str, Any]:
        return self.__mech_params
    
    @pyqtSlot()
    def on_rename_button_clicked(self):
        """Show up a string input to change the data name."""
        row = self.collections_list.currentRow()
        if not row > -1:
            return
        name, ok = QInputDialog.getText(self,
            "Profile name",
            "Please enter the profile name:"
        )
        if not ok:
            return
        if not name:
            QMessageBox.warning(self,
                "Profile name",
                "Can not use blank string to rename."
            )
            return
        item = self.collections_list.item(row)
        self.collections[name] = self.collections.pop(item.text())
        item.setText(name)
    
    @pyqtSlot()
    def on_copy_button_clicked(self):
        """Ask a name to copy a data."""
        row = self.collections_list.currentRow()
        if not row > -1:
            return
        name, ok = QInputDialog.getText(self,
            "Profile name",
            "Please enter a new profile name:"
        )
        if not ok:
            return
        if not name:
            QMessageBox.warning(self,
                "Profile name",
                "Can not use blank string to rename."
            )
            return
        name_old = self.collections_list.item(row).text()
        self.collections[name] = self.collections[name_old].copy()
        self.collections_list.addItem(name)
    
    @pyqtSlot()
    def on_delete_button_clicked(self):
        """Delete a data."""
        row = self.collections_list.currentRow()
        if not row > -1:
            return
        reply = QMessageBox.question(self,
            "Delete",
            "Do you want to delete this structure?"
        )
        if reply != QMessageBox.Yes:
            return
        item = self.collections_list.takeItem(row)
        del self.collections[item.text()]
        self.PreviewCanvas.clear()
        self.__hasCollection()
    
    @pyqtSlot(str)
    @pyqtSlot(QListWidgetItem)
    def __chooseCommon(self, p0: Union[str, QListWidgetItem, None] = None):
        """Update preview canvas for common data."""
        item = self.common_list.currentItem()
        if not item:
            return
        self.__name_loaded = item.text()
        if self.__name_loaded == "Four bar linkage mechanism":
            self.__mech_params = deepcopy(_mech_params_4Bar)
        elif self.__name_loaded == "Eight bar linkage mechanism":
            self.__mech_params = deepcopy(_mech_params_8Bar)
        elif self.__name_loaded == "Ball lifter linkage mechanism":
            self.__mech_params = deepcopy(_mech_params_BallLifter)
        self.PreviewCanvas.from_profile(self.__mech_params)
    
    @pyqtSlot(str)
    @pyqtSlot(QListWidgetItem)
    def __chooseCollections(self, p0: Union[str, QListWidgetItem, None] = None):
        """Update preview canvas for a workbook data."""
        item = self.collections_list.currentItem()
        if not item:
            return
        self.__name_loaded = item.text()
        self.__mech_params = deepcopy(self.collections[self.__name_loaded])
        self.PreviewCanvas.from_profile(self.__mech_params)
    
    @pyqtSlot()
    def on_workbook_button_clicked(self):
        """Get a collection data from current mechanism."""
        try:
            collection = self.getCollection()
        except ValueError as e:
            QMessageBox.warning(self, "Mechanism not support.", str(e))
        else:
            num = 0
            while "mechanism{}".format(num) in self.collections:
                num += 1
            name = "mechanism{}".format(num)
            self.collections[name] = collection.copy()
            self.collections_list.addItem(name)
    
    @pyqtSlot()
    @pyqtSlot(QListWidgetItem)
    def __loadCommon(self, p0: Optional[QListWidgetItem] = None):
        """Load a common data and close."""
        self.__chooseCommon()
        self.accept()
    
    @pyqtSlot()
    @pyqtSlot(QListWidgetItem)
    def __loadCollections(self, p0: Optional[QListWidgetItem] = None):
        """Load a workbook data and close."""
        self.__chooseCollections()
        self.accept()
