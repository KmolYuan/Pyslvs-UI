# -*- coding: utf-8 -*-

"""This module contain all the Qt objects we needed.

Customized class will define below.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence, Union
from math import (
    radians,
    sin,
    cos,
    atan2,
)
from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QCoreApplication,
    QDir,
    QFileInfo,
    QModelIndex,
    QMutex,
    QMutexLocker,
    QObject,
    QPoint,
    QPointF,
    QRectF,
    QSettings,
    QSize,
    QSizeF,
    QStandardPaths,
    QThread,
    QTimer,
    QUrl,
    Qt,
)
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDial,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QGraphicsScene,
    QGraphicsView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressDialog,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QSplashScreen,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTableWidgetSelectionRange,
    QTextEdit,
    QToolTip,
    QUndoCommand,
    QUndoStack,
    QUndoView,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QDesktopServices,
    QFont,
    QIcon,
    QImage,
    QKeySequence,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
    QTextCursor,
)
from PyQt5.QtChart import (
    QCategoryAxis,
    QChart,
    QChartView,
    QLineSeries,
    QScatterSeries,
    QValueAxis,
)
from PyQt5.QtCore import qVersion, PYQT_VERSION_STR

__all__ = [
    'pyqtSignal',
    'pyqtSlot',
    'qVersion',
    'PYQT_VERSION_STR',
    'QAbstractItemView',
    'QAction',
    'QApplication',
    'QBrush',
    'QCategoryAxis',
    'QChart',
    'QChartView',
    'QCheckBox',
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
    'QFileDialog',
    'QFileInfo',
    'QFont',
    'QGraphicsScene',
    'QGraphicsView',
    'QIcon',
    'QImage',
    'QInputDialog',
    'QKeySequence',
    'QLabel',
    'QLineEdit',
    'QLineSeries',
    'QListWidget',
    'QListWidgetItem',
    'QMainWindow',
    'QMenu',
    'QMessageBox',
    'QModelIndex',
    'QMutex',
    'QMutexLocker',
    'QObject',
    'QPainter',
    'QPainterPath',
    'QPen',
    'QPixmap',
    'QPoint',
    'QPointF',
    'QPolygonF',
    'QProgressDialog',
    'QPushButton',
    'QRectF',
    'QBoaderPolygonF',
    'QScatterSeries',
    'QSettings',
    'QSize',
    'QSizeF',
    'QSizePolicy',
    'QSpinBox',
    'QSplashScreen',
    'QStandardPaths',
    'QTabWidget',
    'QTableWidget',
    'QTableWidgetItem',
    'QTableWidgetSelectionRange',
    'QTextCursor',
    'QTextEdit',
    'QThread',
    'QTimer',
    'QToolTip',
    'QUndoCommand',
    'QUndoStack',
    'QUndoView',
    'QUrl',
    'QValueAxis',
    'QVBoxLayout',
    'QWidget',
    'Qt',
]


class QBoaderPolygonF(QPainterPath):
    
    """Reality of a rounded polygon path generator."""
    
    def __init__(self, centers: Sequence[Union[QPoint, QPointF]], radius: float = 10):
        """Initialized with empty list."""
        super(QBoaderPolygonF, self).__init__()
        
        def intersection(
            line1: Tuple[Tuple[float, float], Tuple[float, float]],
            line2: Tuple[Tuple[float, float], Tuple[float, float]]
        ) -> Tuple[float, float]:
            """Determine the intersection by line values."""
            
            def line(
                p1: Tuple[float, float],
                p2: Tuple[float, float]
            ) -> Tuple[float, float, float]:
                """Line values."""
                return (
                    (p1[1] - p2[1]),
                    (p2[0] - p1[0]),
                    -(p1[0]*p2[1] - p2[0]*p1[1])
                )
            
            line1 = line(line1[0], line1[1])
            line2 = line(line2[0], line2[1])
            d = line1[0] * line2[1] - line1[1] * line2[0]
            dx = line1[2] * line2[1] - line1[1] * line2[2]
            dy = line1[0] * line2[2] - line1[2] * line2[0]
            if abs(d) > 0.2:
                x = dx / d
                y = dy / d
                return x, y
            else:
                return False
        
        pt_count = len(centers)
        boundary = []
        for i in range(pt_count):
            p1 = centers[i]
            p2 = centers[i + 1 if (i + 1) < pt_count else 0]
            alpha = atan2(p2.y() - p1.y(), p2.x() - p1.x()) - radians(90)
            offset_x = radius * cos(alpha)
            offset_y = radius * sin(alpha)
            boundary.append((
                (p1.x() + offset_x, p1.y() + offset_y),
                (p2.x() + offset_x, p2.y() + offset_y)
            ))
        
        for i, (p1, p2) in enumerate(boundary):
            if i == 0:
                self.moveTo(*p1)
            self.lineTo(*p2)
            next_line = boundary[(i + 1) % pt_count]
            nx, ny = next_line[0]
            try:
                ix, iy = intersection((p1, p2), next_line)
            except TypeError:
                self.lineTo(nx, ny)
            else:
                self.quadTo(ix, iy, nx, ny)
        self.lineTo(*boundary[0][0])
