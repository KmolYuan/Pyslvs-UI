# -*- coding: utf-8 -*-

"""'collections' module contains
the result from type synthesis and triangular iteration by users.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    TYPE_CHECKING,
    List,
    Tuple,
    Dict,
    Any,
)
from core.QtModules import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QIcon,
    QPixmap,
)
from .structure_widget import StructureWidget
from .configure_widget import ConfigureWidget
from .dialogs import CollectionsDialog

if TYPE_CHECKING:
    from core.widgets import MainWindowBase

__all__ = [
    'Collections',
    'StructureWidget',
    'ConfigureWidget',
    'CollectionsDialog',
]


class Collections(QWidget):

    """Just a widget contains a sub tab widget."""

    def __init__(self, parent: 'MainWindowBase'):
        """Create two widget page and using main window to make their parent."""
        super(Collections, self).__init__(parent)
        layout = QVBoxLayout(self)
        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)
        self.setWindowIcon(QIcon(QPixmap(":/icons/collections.png")))
        self.StructureWidget = StructureWidget(parent)
        self.ConfigureWidget = ConfigureWidget(
            self.StructureWidget.add_collection,
            parent
        )
        tab_widget.addTab(
            self.StructureWidget,
            self.StructureWidget.windowIcon(),
            "Structures"
        )
        tab_widget.addTab(
            self.ConfigureWidget,
            self.ConfigureWidget.windowIcon(),
            "Configuration"
        )
        self.StructureWidget.configure_button.clicked.connect(
            lambda: tab_widget.setCurrentIndex(1)
        )
        self.StructureWidget.layout_sender.connect(
            self.ConfigureWidget.set_graph
        )

    def clear(self):
        """Clear the sub-widgets."""
        self.StructureWidget.clear()
        self.ConfigureWidget.clear()

    def collect_data(self) -> List[Tuple[Tuple[int, int], ...]]:
        """Return collections to database."""
        return [tuple(G.edges) for G in self.StructureWidget.collections]

    def triangle_data(self) -> Dict[str, Dict[str, Any]]:
        """Return profiles to database."""
        return self.ConfigureWidget.collections
