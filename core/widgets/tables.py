# -*- coding: utf-8 -*-

"""Custom table of Points and Links.
Also contains selection status label.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from abc import abstractmethod
from time import time
from typing import (
    Tuple,
    List,
    Dict,
    Iterator,
    Sequence,
    Union,
    Optional,
    Any,
)
from core.QtModules import (
    pyqtSignal,
    Qt,
    QTimer,
    QTableWidget,
    QSizePolicy,
    QAbstractItemView,
    QTableWidgetItem,
    pyqtSlot,
    QApplication,
    QTableWidgetSelectionRange,
    QLabel,
    QWidget,
    QAbcMeta,
)
from core.graphics import colorIcon, colorQt
from core.libs import VPoint, VLink


class _BaseTableWidget(QTableWidget, metaclass=QAbcMeta):
    
    """Two tables has some shared function."""
    
    rowSelectionChanged = pyqtSignal(list)
    deleteRequest = pyqtSignal()
    
    def __init__(self, row: int, headers: Sequence[str], parent: QWidget):
        super(_BaseTableWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setStatusTip("This table will show about the entities items in current view mode.")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        self.setRowCount(row)
        self.setColumnCount(len(headers))
        for i, e in enumerate(headers):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(e))
        
        self.itemSelectionChanged.connect(self.__emitSelectionChanged)
    
    def rowTexts(self, row: int, *, has_name: bool = False) -> List[str]:
        """Get the whole row of texts.
        
        + Edit point: has_name = False
        + Edit link: has_name = True
        """
        texts = []
        for column in self.effectiveRange(has_name):
            item = self.item(row, column)
            if item is None:
                texts.append('')
            else:
                texts.append(item.text())
        return texts
    
    @abstractmethod
    def data(self) -> Iterator[Any]:
        """Return table data in subclass."""
        ...
    
    def dataTuple(self) -> Tuple[Union[VPoint, VLink]]:
        """Return data set as a container."""
        return tuple(self.data())
    
    def selectedRows(self) -> List[int]:
        """Get what row is been selected."""
        return [row for row in range(self.rowCount()) if self.item(row, 0).isSelected()]
    
    def setSelections(self, selections: Sequence[int], key_detect: bool):
        """Auto select function, get the signal from canvas."""
        self.setFocus()
        keyboard_modifiers = QApplication.keyboardModifiers()
        if key_detect:
            continue_select, not_select = {
                Qt.ShiftModifier: (True, False),
                Qt.ControlModifier: (True, True),
            }.get(keyboard_modifiers, (False, False))
            self.__setSelectedRanges(
                selections,
                continue_select=continue_select,
                un_select=not_select
            )
        else:
            self.__setSelectedRanges(
                selections,
                continue_select=(keyboard_modifiers == Qt.ShiftModifier),
                un_select=False
            )
    
    def __setSelectedRanges(
        self,
        selections: Sequence[int],
        *,
        continue_select: bool,
        un_select: bool
    ):
        """Different mode of select function."""
        selected_rows = self.selectedRows()
        if not continue_select:
            self.clearSelection()
        self.setCurrentCell(selections[-1], 0)
        for row in selections:
            is_selected = (row not in selected_rows) if un_select else True
            self.setRangeSelected(
                QTableWidgetSelectionRange(row, 0, row, self.columnCount()-1),
                is_selected
            )
            self.scrollToItem(self.item(row, 0))
    
    def keyPressEvent(self, event):
        """Hit the delete key,
        will emit delete signal from this table.
        """
        if event.key() == Qt.Key_Delete:
            self.deleteRequest.emit()
    
    def clear(self):
        """Overridden the clear function, just removed all items."""
        for row in range(self.rowCount()):
            self.removeRow(0)
    
    @pyqtSlot()
    def clearSelection(self):
        """Overridden the 'clearSelection' slot to emit 'rowSelectionChanged'"""
        super(_BaseTableWidget, self).clearSelection()
        self.rowSelectionChanged.emit([])
    
    @pyqtSlot()
    def __emitSelectionChanged(self):
        """Let canvas to show the point selections."""
        self.rowSelectionChanged.emit(self.selectedRows())


class PointTableWidget(_BaseTableWidget):
    
    """Custom table widget for points."""
    
    selectionLabelUpdate = pyqtSignal(list)
    
    def __init__(self, parent: QWidget):
        super(PointTableWidget, self).__init__(0, (
            'Number',
            'Links',
            'Type',
            'Color',
            'X',
            'Y',
            'Current',
        ), parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 90)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 60)
        self.setColumnWidth(6, 130)
    
    def data(self) -> Iterator[VPoint]:
        """Yield the digitization of all table data."""
        for row in range(self.rowCount()):
            links = self.item(row, 1).text()
            color = self.item(row, 3).text()
            x = float(self.item(row, 4).text())
            y = float(self.item(row, 5).text())
            # p_type = (type: str, angle: float)
            p_type = self.item(row, 2).text().split(':')
            if p_type[0] == 'R':
                type_int = 0
                angle = 0.
            else:
                angle = float(p_type[1])
                type_int = 1 if p_type[0] == 'P' else 2
            vpoint = VPoint(links, type_int, angle, color, x, y, colorQt)
            vpoint.move(*self.currentPosition(row))
            yield vpoint
    
    def expression(self) -> str:
        """Return expression string."""
        exprs = ", ".join(vpoint.expr for vpoint in self.data())
        return f"M[{exprs}]"
    
    def editArgs(
        self,
        row: int,
        links: str,
        type_str: str,
        color: str,
        x: float,
        y: float
    ):
        """Edit a point."""
        for i, e in enumerate([f'Point{row}', links, type_str, color, x, y, f"({x}, {y})"]):
            item = QTableWidgetItem(str(e))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i == 3:
                item.setIcon(colorIcon(e))
            self.setItem(row, i, item)
    
    def rename(self, row: int):
        """When index changed, the points need to rename."""
        for j in range(row, self.rowCount()):
            self.setItem(j, 0, QTableWidgetItem(f'Point{j}'))
    
    def currentPosition(self, row: int) -> List[Tuple[float, float]]:
        """Get the current coordinate from a point."""
        type_str = self.item(row, 2).text().split(':')
        coords_text = self.item(row, 6).text().replace(';', ',')
        coords = eval(f"[{coords_text}]")
        if (type_str[0] in ('P', 'RP')) and (len(coords) == 1):
            x, y = coords[0]
            self.item(row, 6).setText(f"({x}, {y}); ({x}, {y})")
            coords.append(coords[0])
        return coords
    
    def updateCurrentPosition(self, coords: Sequence[Tuple[float, float]]):
        """Update the current coordinate for a point."""
        for i, c in enumerate(coords):
            if type(c[0]) == float:
                text = f"({c[0]}, {c[1]})"
            else:
                text = "; ".join(f"({x}, {y})" for x, y in c)
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.setItem(i, 6, item)
    
    def getBackPosition(self):
        """Let all the points go back to origin coordinate."""
        self.updateCurrentPosition(tuple(
            (float(self.item(row, 4).text()), float(self.item(row, 5).text()))
            for row in range(self.rowCount())
        ))
    
    def getLinks(self, row: int) -> List[str]:
        item = self.item(row, 1)
        if not item:
            return []
        return [s for s in item.text().split(',') if s]
    
    def setSelections(self, selections: Sequence[int], key_detect: bool):
        super(PointTableWidget, self).setSelections(selections, key_detect)
        self.selectionLabelUpdate.emit(self.selectedRows())
    
    def effectiveRange(self, has_name: bool):
        """Row range that can be delete."""
        if has_name:
            return range(self.columnCount())
        else:
            return range(1, self.columnCount() - 1)
    
    @pyqtSlot()
    def clearSelection(self):
        """Overridden the 'clearSelection' slot,
        so it will emit signal to clean the selection.
        """
        super(PointTableWidget, self).clearSelection()
        self.selectionLabelUpdate.emit([])


class LinkTableWidget(_BaseTableWidget):
    
    """Custom table widget for link."""
    
    def __init__(self, parent: QWidget):
        super(LinkTableWidget, self).__init__(1, ('Name', 'Color', 'Points'), parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)
        self.editArgs(0, 'ground', 'White', '')
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 130)
    
    def data(self) -> Iterator[VLink]:
        """Yield the digitization of all table data."""
        for row in range(self.rowCount()):
            name = self.item(row, 0).text()
            color = self.item(row, 1).text()
            points = []
            for p in self.item(row, 2).text().split(','):
                if not p:
                    continue
                points.append(int(p.replace('Point', '')))
            yield VLink(name, color, tuple(points), colorQt)
    
    def dataDict(self) -> Dict[str, str]:
        """Return name and color as a dict."""
        return {vlink.name: vlink.colorSTR for vlink in self.data()}
    
    def editArgs(
        self,
        row: int,
        name: str,
        color: str,
        points: str
    ):
        """Edite a link."""
        for i, e in enumerate((name, color, points)):
            item = QTableWidgetItem(e)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i == 1:
                item.setIcon(colorIcon(e))
            self.setItem(row, i, item)
    
    def findName(self, name: str) -> int:
        """Return row index by input name."""
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if not item:
                continue
            if name == item.text():
                return row
    
    def getPoints(self, row: int) -> List[int]:
        """Get all point names."""
        item = self.item(row, 2)
        if not item:
            return []
        return [int(s.replace('Point', '')) for s in item.text().split(',') if s]
    
    def effectiveRange(self, has_name: bool):
        """Row range that can be delete."""
        del has_name
        return range(self.columnCount())
    
    def clear(self):
        """We should keep the 'ground' left."""
        super(LinkTableWidget, self).clear()
        self.setRowCount(1)
        self.editArgs(0, 'ground', 'White', '')


class ExprTableWidget(_BaseTableWidget):
    
    """Expression table.
    
    + Freemove request: link name, length
    """
    
    reset = pyqtSignal(bool)
    freemove_request = pyqtSignal(bool)
    
    def __init__(self, parent: QWidget):
        column_count = ('Function', 'p0', 'p1', 'p2', 'p3', 'p4', 'target')
        super(ExprTableWidget, self).__init__(0, column_count, parent)
        for column in range(self.columnCount()):
            self.setColumnWidth(column, 80)
        self.exprs = []
        
        @pyqtSlot(QTableWidgetItem)
        def adjust_request(item: QTableWidgetItem):
            """This function is use to change link length
            without to drag the points.
            """
            if item:
                self.freemove_request.emit(item.text().startswith('L'))
            else:
                self.freemove_request.emit(False)
        
        # Double click behavior.
        self.currentItemChanged.connect(adjust_request)
    
    def setExpr(
        self,
        exprs: List[Tuple[str]],
        data_dict: Dict[str, Union[Tuple[float, float], float]],
        unsolved: Tuple[int]
    ):
        """Set the table items for new coming expression."""
        if exprs != self.exprs:
            self.clear()
            self.setRowCount(len(exprs) + len(unsolved))
        row = 0
        for expr in exprs:
            # Target
            self.setItem(row, self.columnCount() - 1, QTableWidgetItem(expr[-1]))
            # Parameters
            for column, e in enumerate(expr[:-1]):
                if e in data_dict:
                    if type(data_dict[e]) == float:
                        # Pure digit
                        text = f"{e}:{data_dict[e]:.02f}"
                    else:
                        # Coordinate
                        text = f"{e}:({data_dict[e][0]:.02f}, {data_dict[e][1]:.02f})"
                else:
                    # Function name
                    text = e
                item = QTableWidgetItem(text)
                item.setToolTip(text)
                self.setItem(row, column, item)
            row += 1
        for p in unsolved:
            # Declaration
            self.setItem(row, 0, QTableWidgetItem("Unsolved"))
            # Target
            self.setItem(row, self.columnCount() - 1, QTableWidgetItem(f"P{p}"))
            row += 1
        self.exprs = exprs
    
    def data(self) -> None:
        """Not used generator."""
        return
    
    def clear(self):
        """Emit to close the link free move widget."""
        super(ExprTableWidget, self).clear()
        self.reset.emit(False)


class SelectionLabel(QLabel):
    
    """This QLabel can show distance in status bar."""
    
    def __init__(self, parent: QWidget):
        super(SelectionLabel, self).__init__(parent)
        self.updateSelectPoint()
        self.dataTuple = parent.EntitiesPoint.dataTuple
    
    @pyqtSlot()
    @pyqtSlot(list)
    def updateSelectPoint(self, points: Optional[List[int]] = None):
        """Get points and distance from Point table widget."""
        if points is None:
            points = []
        p_count = len(points)
        if not p_count:
            self.setText("No selection.")
            return
        text = ""
        text += "Selected: "
        text += " - ".join(str(p) for p in points)
        vpoints = self.dataTuple()
        if p_count > 1:
            distances = []
            angles = []
            for i in range(p_count):
                if i != 0:
                    vpoint0 = vpoints[points[i - 1]]
                    vpoint1 = vpoints[points[i]]
                    distances.append(f"{vpoint1.distance(vpoint0):.04}")
                    angles.append(f"{vpoint0.slope_angle(vpoint1):.04}°")
            ds_t = ", ".join(distances)
            as_t = ", ".join(angles)
            text += f" | {ds_t} | {as_t}"
        self.setText(text)
    
    @pyqtSlot(float, float)
    def updateMousePosition(self, x: float, y: float):
        """Get the mouse position from canvas when press the middle button."""
        self.setText(f"Mouse at: ({x:.04f}, {y:.04f})")


class FPSLabel(QLabel):
    
    """This QLabel can show FPS of main canvas in status bar."""
    
    def __init__(self, parent: QWidget):
        super(FPSLabel, self).__init__(parent)
        self.__t0 = time() - 1
        self.__frame_timer = QTimer(self)
        self.__frame_timer.timeout.connect(self.__updateText)
        self.__frame_timer.start(500)
    
    @pyqtSlot()
    def __updateText(self):
        """Update FPS with timer."""
        t1 = time() - self.__t0
        fps = 1 / t1 if t1 else 1
        self.setText(f"FPS: {fps:6.02f}")
    
    @pyqtSlot()
    def updateText(self):
        """Update FPS with timer."""
        self.__updateText()
        self.__t0 = time()
