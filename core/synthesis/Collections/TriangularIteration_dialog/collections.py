# -*- coding: utf-8 -*-

"""The option dialog to load the structure data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QDialog,
    Qt,
    QDialogButtonBox,
    pyqtSlot,
    QInputDialog,
    QMessageBox,
    QListWidgetItem,
)
from core.graphics import PreviewCanvas, replace_by_dict
from copy import deepcopy
from typing import Tuple
from .Ui_collections import Ui_Dialog

mechanismParams_4Bar = {
    'Driver': {'A': None}, #'A':(x, y, r)
    'Follower': {'B': None}, #'B':(x, y, r)
    'Target': {'E': None}, #'E':((x1, y1), (x2, y2), (x3, y3), ...)
    'Link_Expression': "ground[A,B];[A,C];[C,D,E];[B,D]",
    'Expression': "PLAP[A,L0,a0,B](C);PLLP[C,L1,L2,B](D);PLLP[C,L3,L4,D](E)",
    'constraint': [('A', 'B', 'C', 'D')],
    'Graph': ((0, 1), (1, 2), (2, 3), (3, 0)),
    'name_dict': {
        'A': 'P0',
        'B': 'P1',
        'C': 'P2',
        'D': 'P3',
        'E': 'P4'
    },
    'pos': {
        0: (-70, -70),
        1: (70, -70),
        2: (-70, 12.5),
        3: (70, 12.5),
        4: (0, 63.5)
    },
    'cus': {'P4': 2},
    'same': {}
}

mechanismParams_8Bar = {
    'Driver': {'A': None},
    'Follower': {'B': None},
    'Target': {'H': None},
    'Link_Expression': "ground[A,B];[A,C];[C,D];[C,F];[B,D,E];[B,F];[E,G];[F,G,H]",
    'Expression': "PLAP[A,L0,a0,B](C);PLLP[B,L2,L1,C](D);PLLP[B,L4,L3,D](E);" +
        "PLLP[C,L5,L6,B](F);PLLP[F,L8,L7,E](G);PLLP[F,L9,L10,G](H)",
    'constraint': [('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'F')],
    'Graph': ((0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 4), (3, 5), (3, 7), (4, 6), (6, 7)),
    'name_dict': {
        'A': 'P0',
        'B': 'P1',
        'C': 'P3',
        'D': 'P5',
        'E': 'P8',
        'F': 'P7',
        'G': 'P9',
        'H': 'P10',
        'I': 'P2',
        'J': 'P4',
        'K': 'P6'
    },
    'pos':{
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
        10: (32.5, -107.5)
    },
    'cus':{'P10': 7},
    'same':{2: 1, 4: 3, 6: 7}
}

mechanismParams_BallLifter = {
    'Driver': {'A': None},
    'Follower': {
        'B': None,
        'D': None,
        'I': None,
        'L': None
    },
    'Target': {
        'N': None,
        'H': None
    },
    'Link_Expression': "ground[A,B,D,I,L];[A,C];[C,J,K];[C,E,F];[I,J];" +
        "[K,M,N];[L,M];[D,E];[F,G,H];[B,G]",
    'Expression': "PLAP[A,L0,a0,B](C);PLLP[C,L1,L2,D](E);PLLP[C,L3,L4,E](F);" +
        "PLLP[F,L5,L6,B](G);PLLP[F,L7,L8,G](H);PLLP[I,L9,L10,C](J);" +
        "PLLP[J,L11,L12,C](K);PLLP[K,L13,L14,L](M);PLLP[K,L15,L16,M](N)",
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
        14: (44.12, 107.65)
    },
    'constraint': [('A', 'C', 'J', 'I'), ('A', 'C', 'E', 'D')],
    'Graph': ((0, 1), (0, 4), (0, 6), (0, 7), (0, 9), (1, 2), (1, 3), (2, 4),
        (2, 5), (3, 7), (3, 8), (5, 6), (8, 9)),
    'name_dict': {
        'A': 'P0',
        'B': 'P4',
        'C': 'P5',
        'D': 'P3',
        'E': 'P9',
        'F': 'P10',
        'G': 'P12',
        'H': 'P14',
        'I': 'P1',
        'J': 'P7',
        'K': 'P8',
        'L': 'P2',
        'M': 'P11',
        'N': 'P13',
        'O': 'P6'
    },
    'cus': {'P13': 5, 'P14': 8},
    'same': {6: 5}
}

class CollectionsDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Load the settings after closed.
    """
    
    def __init__(self, parent):
        super(CollectionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
            self.windowFlags() &
            ~Qt.WindowContextHelpButtonHint |
            Qt.WindowMaximizeButtonHint
        )
        self.collections = parent.collections
        self.name_loaded = ""
        
        def get_solutions_func() -> Tuple[str]:
            """Return solutions to preview canvas."""
            try:
                return replace_by_dict(self.collections[self.name_loaded])
            except KeyError:
                if self.name_loaded == "Four bar linkage mechanism":
                    return replace_by_dict(mechanismParams_4Bar)
                elif self.name_loaded == "Eight bar linkage mechanism":
                    return replace_by_dict(mechanismParams_8Bar)
                elif self.name_loaded == "Ball lifter linkage mechanism":
                    return replace_by_dict(mechanismParams_BallLifter)
                else:
                    return tuple()
        
        self.PreviewCanvas = PreviewCanvas(get_solutions_func, self)
        self.preview_layout.addWidget(self.PreviewCanvas)
        self.show_solutions.clicked.connect(self.PreviewCanvas.setShowSolutions)
        for name in self.collections:
            self.collections_list.addItem(name)
        #Splitter
        self.main_splitter.setSizes([200, 200])
        #Signals
        self.common_list.currentTextChanged.connect(self.choose_common)
        self.common_list.itemClicked.connect(self.choose_common)
        self.common_load.clicked.connect(self.load_common)
        self.common_list.itemDoubleClicked.connect(self.load_common)
        self.collections_list.currentTextChanged.connect(self.choose_collections)
        self.collections_list.itemClicked.connect(self.choose_collections)
        self.buttonBox.accepted.connect(self.load_collections)
        self.collections_list.itemDoubleClicked.connect(self.load_collections)
        self.collections_list.currentRowChanged.connect(self.canOpen)
        self.hasCollection()
        self.canOpen()
    
    def canOpen(self):
        """Set the button box to enable when data is already."""
        self.buttonBox.button(QDialogButtonBox.Open) \
        .setEnabled(self.collections_list.currentRow() > -1)
    
    def hasCollection(self):
        """Set the buttons to enable when user choose a data."""
        hasCollection = bool(self.collections)
        for button in [
            self.rename_button,
            self.copy_button,
            self.delete_button
        ]:
            button.setEnabled(hasCollection)
    
    @pyqtSlot()
    def on_rename_button_clicked(self):
        """Show up a string input to change the data name."""
        row = self.collections_list.currentRow()
        if not row>-1:
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
        if not row>-1:
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
        if not row>-1:
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
        self.hasCollection()
    
    @pyqtSlot(str)
    @pyqtSlot(QListWidgetItem)
    def choose_common(self, p0=None):
        """Update preview canvas for common data."""
        text = self.common_list.currentItem().text()
        if not text:
            return
        self.name_loaded = text
        if text == "Four bar linkage mechanism":
            self.mechanismParams = deepcopy(mechanismParams_4Bar)
        elif text == "Eight bar linkage mechanism":
            self.mechanismParams = deepcopy(mechanismParams_8Bar)
        elif self.name_loaded == "Ball lifter linkage mechanism":
            self.mechanismParams = deepcopy(mechanismParams_BallLifter)
        self.PreviewCanvas.from_profile(self.mechanismParams)
    
    @pyqtSlot(str)
    @pyqtSlot(QListWidgetItem)
    def choose_collections(self, p0=None):
        """Update preview canvas for a workbook data."""
        text = self.collections_list.currentItem().text()
        if not text:
            return
        self.name_loaded = text
        self.mechanismParams = self.collections[self.name_loaded]
        self.PreviewCanvas.from_profile(self.mechanismParams)
    
    @pyqtSlot()
    @pyqtSlot(QListWidgetItem)
    def load_common(self, p0=None):
        """Load a common data and close."""
        self.choose_common(self.common_list.currentItem().text())
        self.accept()
    
    @pyqtSlot()
    @pyqtSlot(QListWidgetItem)
    def load_collections(self, p0=None):
        """Load a workbook data and close."""
        self.choose_collections(self.collections_list.currentItem().text())
        self.accept()
    
    @pyqtSlot(bool)
    def on_switch_name_clicked(self, checked):
        """Switch name dict of preview canvas."""
        if checked:
            self.PreviewCanvas.setNameDict({})
        else:
            self.PreviewCanvas.setNameDict(self.mechanismParams['name_dict'])
