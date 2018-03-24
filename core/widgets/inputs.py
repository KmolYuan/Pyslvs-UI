# -*- coding: utf-8 -*-

"""The widget of 'Inputs' tab."""

from core.QtModules import (
    pyqtSlot,
    QWidget,
    QDial,
    QTimer,
    QMenu,
    QMessageBox,
    QInputDialog,
    QListWidgetItem,
    QPoint,
    QApplication,
)
from core.io import (
    AddVariable, DeleteVariable,
    AddPath, DeletePath,
)
import csv
from typing import Tuple
from .rotatable import RotatableView
from .Ui_inputs import Ui_Form

class InputsWidget(QWidget, Ui_Form):
    
    """There has following functions:
    
    + Function of mechanism variables settings.
    + Path recording.
    """
    
    def __init__(self, parent):
        super(InputsWidget, self).__init__(parent)
        self.setupUi(self)
        #parent's pointer.
        self.FreeMoveMode = parent.FreeMoveMode
        self.Entities_Point = parent.Entities_Point
        self.Entities_Link = parent.Entities_Link
        self.DynamicCanvasView = parent.DynamicCanvasView
        self.resolve = parent.resolve
        self.reload_canvas = parent.reload_canvas
        self.outputTo = parent.outputTo
        self.ConflictGuide = parent.ConflictGuide
        self.DOF = lambda: parent.DOF
        self.CommandStack = parent.CommandStack
        #self widgets.
        self.inputs_Degree = QDial()
        self.inputs_Degree.setEnabled(False)
        self.inputs_Degree.valueChanged.connect(self.variableValueUpdate)
        self.inputs_dial_layout.addWidget(RotatableView(self.inputs_Degree))
        self.inputs_variable_stop.clicked.connect(self.variableValueReset)
        self.inputs_playShaft = QTimer(self)
        self.inputs_playShaft.setInterval(10)
        self.inputs_playShaft.timeout.connect(self.inputs_change_index)
        '''Inputs record context menu
        
        + Copy data from Point{}
        + ...
        '''
        self.inputs_record.customContextMenuRequested.connect(
            self.on_inputs_record_context_menu
        )
        self.popMenu_inputs_record = QMenu(self)
        self.clear()
    
    def clear(self):
        self.pathData = {}
        self.inputs_record.clear()
        self.inputs_variable.clear()
    
    @pyqtSlot(tuple)
    def inputs_points_setSelection(self, selections):
        """Set one selection from canvas."""
        self.inputs_points.setCurrentRow(
            selections[0]
            if selections[0] in self.Entities_Point.selectedRows()
            else -1
        )
    
    @pyqtSlot()
    def inputs_points_clearSelection(self):
        """Clear the points selection."""
        self.inputs_points.setCurrentRow(-1)
    
    @pyqtSlot(int)
    def on_inputs_points_currentRowChanged(self, row: int):
        """Change the point row from input widget."""
        self.inputs_baseLinks.clear()
        if not row > -1:
            return
        if row not in self.Entities_Point.selectedRows():
            self.Entities_Point.setSelections((row,), False)
        for linkName in self.Entities_Point.item(row, 1).text().split(','):
            if not linkName:
                continue
            self.inputs_baseLinks.addItem(linkName)
    
    @pyqtSlot(int)
    def on_inputs_baseLinks_currentRowChanged(self, row: int):
        """Set the drive links from base link."""
        self.inputs_driveLinks.clear()
        if not row > -1:
            return
        inputs_point = self.inputs_points.currentRow()
        linkNames = self.Entities_Point.item(inputs_point, 1).text().split(',')
        for linkName in linkNames:
            if linkName == self.inputs_baseLinks.currentItem().text():
                continue
            self.inputs_driveLinks.addItem(linkName)
    
    @pyqtSlot(int)
    def on_inputs_driveLinks_currentRowChanged(self, row: int):
        """Set enable of 'add variable' button."""
        if not row > -1:
            self.inputs_variable_add.setEnabled(False)
            return
        typeText = self.inputs_points.currentItem().text().split()[0]
        self.inputs_variable_add.setEnabled(typeText=='[R]')
    
    @pyqtSlot()
    def on_inputs_variable_add_clicked(self):
        """Add inputs variable from click button."""
        self.add_inputs_variable(
            self.inputs_points.currentRow(),
            self.inputs_baseLinks.currentItem().text(),
            self.inputs_driveLinks.currentItem().text()
        )
    
    def add_inputs_variable(self,
        point: int,
        base_link: str,
        drive_links: str
    ):
        """Add variable with '->' sign."""
        if self.inputs_variable.count() >= self.DOF():
            return
        name = 'Point{}'.format(point)
        text = '->'.join([
            name,
            base_link,
            drive_links,
            "{:.02f}".format(self.getLinkAngle(point, drive_links))
        ])
        for variable in self.get_inputs_variables():
            if name == variable[0]:
                return
        self.CommandStack.beginMacro("Add variable of {}".format(name))
        self.CommandStack.push(AddVariable(text, self.inputs_variable))
        self.CommandStack.endMacro()
    
    def add_inputs_variables(self,
        variables: Tuple[Tuple[int, str, str]]
    ):
        """Add from database."""
        for variable in variables:
            self.add_inputs_variable(*variable)
    
    @pyqtSlot(int)
    def on_inputs_variable_currentRowChanged(self, row: int =None):
        """Set the angle of base link and drive link."""
        if row is None:
            row = self.inputs_variable.currentRow()
        enabled = row > -1
        rotatable = enabled and not self.FreeMoveMode.isChecked()
        self.inputs_Degree.setEnabled(rotatable)
        self.oldVariableValue = self.inputs_Degree.value() / 100.
        self.inputs_variable_play.setEnabled(rotatable)
        self.inputs_variable_speed.setEnabled(rotatable)
        self.inputs_Degree.setValue(float(
            self.inputs_variable.currentItem().text().split('->')[-1])*100
            if enabled else 0
        )
    
    def inputs_variable_excluding(self, row: int =None):
        """Remove variable if the point was been deleted.
        
        Default: all.
        """
        one_row = row is not None
        for i, variable in enumerate(self.get_inputs_variables()):
            row_ = variable[0]
            #If this is not origin point any more.
            if one_row and (row != row_):
                continue
            self.CommandStack.beginMacro("Remove variable of Point{}".format(row))
            self.CommandStack.push(DeleteVariable(i, self.inputs_variable))
            self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_inputs_variable_remove_clicked(self):
        """Remove and reset angle."""
        row = self.inputs_variable.currentRow()
        if not row > -1:
            return
        reply = QMessageBox.question(self,
            "Remove variable",
            "Do you want to remove this variable?"
        )
        if reply != QMessageBox.Yes:
            return
        self.inputs_variable_stop.click()
        self.CommandStack.beginMacro("Remove variable of Point{}".format(row))
        self.CommandStack.push(DeleteVariable(row, self.inputs_variable))
        self.CommandStack.endMacro()
        self.Entities_Point.getBackPosition()
        self.resolve()
    
    def getLinkAngle(self, row: int, link: str) -> float:
        """Get the angle of base link and drive link."""
        Point = self.Entities_Point.data()
        Link = self.Entities_Link.data()
        LinkIndex = [vlink.name for vlink in Link]
        relate = Link[LinkIndex.index(link)].points
        base = Point[row]
        drive = Point[relate[relate.index(row)-1]]
        return base.slopeAngle(drive)
    
    def get_inputs_variables(self) -> Tuple[int, str, str, float]:
        """A generator use to get variables."""
        for row in range(self.inputs_variable.count()):
            variable = self.inputs_variable.item(row).text().split('->')
            variable[0] = int(variable[0].replace('Point', ''))
            variable[3] = float(variable[3])
            yield tuple(variable)
    
    def inputs_variable_reload(self):
        """Auto check the points and type."""
        self.inputs_points.clear()
        for i in range(self.Entities_Point.rowCount()):
            text = "[{}] Point{}".format(
                self.Entities_Point.item(i, 2).text(),
                i
            )
            self.inputs_points.addItem(text)
        self.variableValueReset()
    
    def variableValueUpdate(self, value):
        """Update the value when rotating QDial."""
        item = self.inputs_variable.currentItem()
        value /= 100.
        if item:
            itemText = item.text().split('->')
            itemText[-1] = "{:.04f}".format(value)
            item.setText('->'.join(itemText))
            self.resolve()
        interval = self.inputs_record_interval.value()
        if (
            self.inputs_record_record.isChecked() and
            abs(self.oldVariableValue - value) > interval
        ):
            self.DynamicCanvasView.recordPath()
            self.oldVariableValue = value
    
    def variableValueReset(self):
        """Reset the value of QDial."""
        if self.inputs_playShaft.isActive():
            self.inputs_variable_play.setChecked(False)
            self.inputs_playShaft.stop()
        self.Entities_Point.getBackPosition()
        for i, variable in enumerate(self.get_inputs_variables()):
            point = variable[0]
            text = '->'.join([
                'Point{}'.format(point),
                variable[1],
                variable[2],
                "{:.02f}".format(self.getLinkAngle(point, variable[2]))
            ])
            self.inputs_variable.item(i).setText(text)
        self.on_inputs_variable_currentRowChanged()
        self.resolve()
    
    @pyqtSlot(bool)
    def on_inputs_variable_play_toggled(self, toggled):
        """Triggered when play button was changed."""
        self.inputs_Degree.setEnabled(not toggled)
        if toggled:
            self.inputs_playShaft.start()
        else:
            self.inputs_playShaft.stop()
    
    @pyqtSlot()
    def inputs_change_index(self):
        """QTimer change index."""
        index = self.inputs_Degree.value()
        speed = self.inputs_variable_speed.value()
        extremeRebound = (
            self.ConflictGuide.isVisible() and
            self.extremeRebound.isChecked()
        )
        if extremeRebound:
            speed *= -1
            self.inputs_variable_speed.setValue(speed)
        index += int(speed * 6 * (3 if extremeRebound else 1))
        index %= self.inputs_Degree.maximum()
        self.inputs_Degree.setValue(index)
    
    @pyqtSlot(bool)
    def on_inputs_record_record_toggled(self, toggled):
        """Save to file path data."""
        if toggled:
            self.DynamicCanvasView.recordStart(int(
                360 / self.inputs_record_interval.value()
            ))
            return
        path = self.DynamicCanvasView.getRecordPath()
        name, ok = QInputDialog.getText(self,
            "Recording completed!",
            "Please input name tag:"
        )
        if (not name) or (name in self.pathData):
            i = 0
            while "Record_{}".format(i) in self.pathData:
                i += 1
            QMessageBox.information(self,
                "Record",
                "The name tag is being used or empty."
            )
            name = "Record_{}".format(i)
        self.addPath(name, path)
    
    def addPath(self, name: str, path: Tuple[Tuple[float, float]]):
        """Add path function."""
        self.CommandStack.beginMacro("Add {{Path: {}}}".format(name))
        self.CommandStack.push(AddPath(
            self.inputs_record,
            name,
            self.pathData,
            path
        ))
        self.CommandStack.endMacro()
        self.inputs_record.setCurrentRow(self.inputs_record.count() - 1)
    
    def loadPaths(self, paths: Tuple[Tuple[Tuple[float, float]]]):
        """Add multiple path."""
        for name, path in paths.items():
            self.addPath(name, path)
    
    @pyqtSlot()
    def on_inputs_record_remove_clicked(self):
        """Remove path data."""
        row = self.inputs_record.currentRow()
        if not row>-1:
            return
        self.CommandStack.beginMacro("Delete {{Path: {}}}".format(
            self.inputs_record.item(row).text()
        ))
        self.CommandStack.push(DeletePath(
            row,
            self.inputs_record,
            self.pathData
        ))
        self.CommandStack.endMacro()
        self.inputs_record.setCurrentRow(self.inputs_record.count() - 1)
        self.reload_canvas()
    
    @pyqtSlot(QListWidgetItem)
    def on_inputs_record_itemDoubleClicked(self, item):
        """View path data."""
        data = self.pathData[item.text().split(":")[0]]
        reply = QMessageBox.question(
            self,
            "Path data",
            "This path data including {}.".format(", ".join(
                "Point{}".format(i) for i in range(len(data)) if data[i]
            )),
            (QMessageBox.Save | QMessageBox.Close),
            QMessageBox.Close
        )
        if reply != QMessageBox.Save:
            return
        fileName = self.outputTo(
            "path data",
            ["Comma-Separated Values (*.csv)", "Text file (*.txt)"]
        )
        if not fileName:
            return
        with open(fileName, 'w', newline='') as stream:
            writer = csv.writer(stream)
            for point in data:
                for coordinate in point:
                    writer.writerow(coordinate)
                writer.writerow(())
        print("Output path data: {}".format(fileName))
    
    @pyqtSlot(QPoint)
    def on_inputs_record_context_menu(self, point):
        """Show the context menu.
        
        Show path [0], [1], ...
        Or copy path coordinates.
        """
        row = self.inputs_record.currentRow()
        if row > -1:
            action = self.popMenu_inputs_record.addAction("Show all")
            action.index = -1
            data = self.pathData[
                self.inputs_record
                .item(row)
                .text()
                .split(":")[0]
            ]
            for action_text in ("Show", "Copy data from"):
                self.popMenu_inputs_record.addSeparator()
                for i in range(len(data)):
                    if data[i]:
                        action = self.popMenu_inputs_record.addAction(
                            "{} Point{}".format(action_text, i)
                        )
                        action.index = i
        action = self.popMenu_inputs_record.exec_(
            self.inputs_record.mapToGlobal(point)
        )
        if action:
            if "Copy data from" in action.text():
                QApplication.clipboard().setText('\n'.join(
                    "{},{}".format(x, y) for x, y in data[action.index]
                ))
            elif "Show" in action.text():
                if action.index==-1:
                    self.inputs_record_show.setChecked(True)
                self.DynamicCanvasView.setPathShow(action.index)
        self.popMenu_inputs_record.clear()
    
    @pyqtSlot()
    def on_inputs_record_show_clicked(self):
        """Show all paths or hide."""
        if self.inputs_record_show.isChecked():
            show = -1
        else:
            show = -2
        self.DynamicCanvasView.setPathShow(show)
    
    @pyqtSlot(int)
    def on_inputs_record_currentRowChanged(self, row):
        """Reload the canvas when switch the path."""
        if self.inputs_record_show.isChecked():
            self.DynamicCanvasView.setPathShow(-1)
        self.reload_canvas()
