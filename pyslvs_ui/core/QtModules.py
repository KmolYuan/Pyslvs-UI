# -*- coding: utf-8 -*-

"""This module contains all the Qt objects we needed.

Customized class will define below.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from abc import ABCMeta
from qtpy import QtCore, QtGui, QtWidgets, API_NAME
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCharts import QtCharts
if API_NAME == 'PyQt5':
    from PyQt5.QtCore import PYQT_VERSION_STR
    API = f"{API_NAME} {PYQT_VERSION_STR}"
    del PYQT_VERSION_STR
elif API_NAME == 'PySide2':
    from PySide2 import __version__
    API = f"{API_NAME} {__version__}"
    del __version__
else:
    raise ModuleNotFoundError("module not found: PyQt5 or PySide2")
del API_NAME

QT_VERSION = QtCore.__version__

__all__ = [
    'API',
    'QT_VERSION',
    'Qt',
    'QtCore',
    'QtGui',
    'QtWidgets',
    'Signal',
    'Slot',
    'qt_image_format',
    'QABCMeta',
    'QAbstractItemView',
    'QAction',
    'QApplication',
    'QBrush',
    'QtCharts',
    'QCheckBox',
    'QCloseEvent',
    'QColor',
    'QColorDialog',
    'QComboBox',
    'QCoreApplication',
    'QCursor',
    'QDateTime',
    'QDesktopServices',
    'QDial',
    'QDialog',
    'QDialogButtonBox',
    'QDir',
    'QDoubleSpinBox',
    'QDragEnterEvent',
    'QDropEvent',
    'QFile',
    'QFileDevice',
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
    'QLabel',
    'QLineEdit',
    'QLineF',
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
    'QRegion',
    'QSpacerItem',
    'QSplitter',
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
    'QVBoxLayout',
    'QWheelEvent',
    'QWidget',
]


qt_image_format = (
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
        def my_abstract_method(self) -> None:
            ...
    """
    pass


del ABCMeta
