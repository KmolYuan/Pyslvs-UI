# -*- coding: utf-8 -*-

"""This module contains all the Qt objects we needed.

Customized class will define below.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from abc import ABCMeta
from typing import Tuple

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot
QT_VERSION_STR = QtCore.QT_VERSION_STR
PYQT_VERSION_STR = QtCore.PYQT_VERSION_STR

__all__ = [
    'Qt',
    'QtCore',
    'QtGui',
    'QtWidgets',
    'Signal',
    'Slot',
    'qt_image_format',
    'QT_VERSION_STR',
    'PYQT_VERSION_STR',
    'QABCMeta',
    'QAbstractItemView',
    'QAction',
    'QApplication',
    'QBrush',
    'QCategoryAxis',
    'QChart',
    'QChartView',
    'QCheckBox',
    'QCloseEvent',
    'QColor',
    'QColorDialog',
    'QComboBox',
    'QCoreApplication',
    'QCursor',
    'QDesktopServices',
    'QDial',
    'QDialog',
    'QDialogButtonBox',
    'QDir',
    'QDoubleSpinBox',
    'QDragEnterEvent',
    'QDropEvent',
    'QFile',
    'QFileDialog',
    'QFileInfo',
    'QFont',
    'QFontMetrics',
    'QFormLayout',
    'QFrame',
    'QGraphicsScene',
    'QGraphicsView',
    'QGridLayout',
    'QGroupBox',
    'QHBoxLayout',
    'QHeaderView',
    'QIcon',
    'QImage',
    'QInputDialog',
    'QKeyEvent',
    'QKeySequence',
    'QLabel',
    'QLineEdit',
    'QLineF',
    'QLineSeries',
    'QListView',
    'QListWidget',
    'QListWidgetItem',
    'QMainWindow',
    'QMetaObject',
    'QMenu',
    'QMenuBar',
    'QMessageBox',
    'QMimeData',
    'QModelIndex',
    'QMouseEvent',
    'QMutex',
    'QMutexLocker',
    'QObject',
    'QPainter',
    'QPaintEvent',
    'QPainterPath',
    'QPen',
    'QPixmap',
    'QPoint',
    'QPointF',
    'QPolygonF',
    'QProgressBar',
    'QProgressDialog',
    'QPushButton',
    'QRadioButton',
    'QRect',
    'QRectF',
    'QSpacerItem',
    'QSplitter',
    'QScatterSeries',
    'QScrollArea',
    'QScrollBar',
    'QSettings',
    'QShortcut',
    'QSize',
    'QSizeF',
    'QSizePolicy',
    'QSlider',
    'QSpinBox',
    'QSplashScreen',
    'QStandardPaths',
    'QStatusBar',
    'QTabWidget',
    'QTableWidget',
    'QTableWidgetItem',
    'QTableWidgetSelectionRange',
    'QTextBrowser',
    'QTextCursor',
    'QTextEdit',
    'QThread',
    'QTimer',
    'QTreeWidgetItem',
    'QToolButton',
    'QToolBox',
    'QToolTip',
    'QUndoCommand',
    'QUndoStack',
    'QUndoView',
    'QUrl',
    'QValueAxis',
    'QVBoxLayout',
    'QWheelEvent',
    'QWidget',
]


qt_image_format: Tuple[str, ...] = (
    "Portable Network Graphics (*.png)",
    "Joint Photographic Experts Group (*.jpg)",
    "Bitmap Image file (*.bmp)",
    "Business Process Model (*.bpm)",
    "Tagged Image File Format (*.tiff)",
    "Windows Icon (*.ico)",
    "Wireless Application Protocol Bitmap (*.wbmp)",
    "X Bitmap (*.xbm)",
    "X Pixmap (*.xpm)",
)


class QABCMeta(type(QObject), ABCMeta):
    """Qt ABCMeta class.

    Usage:

    class MyQObject(QObject, metaclass=QABCMeta):
        @abstractmethod
        def my_abstract_method(self):
            ...
    """
    pass
