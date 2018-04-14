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
        self.reloadCanvas = parent.reloadCanvas
        self.outputTo = parent.outputTo
        self.ConflictGuide = parent.ConflictGuide
        self.DOF = lambda: parent.DOF
        self.rightInput = parent.rightInput
        self.CommandStack = parent.CommandStack
        #self widgets.
        self.dial = QDial()
        self.dial.setEnabled(False)
        self.dial.valueChanged.connect(self.__variableValueUpdate)
        self.inputs_dial_layout.addWidget(RotatableView(self.dial))
        self.variable_stop.clicked.connect(self.variableValueReset)
        self.inputs_playShaft = QTimer(self)
        self.inputs_playShaft.setInterval(10)
        self.inputs_playShaft.timeout.connect(self.__changeIndex)
        self.variable_list.currentRowChanged.connect(self.__dialOk)
        '''Inputs record context menu
        
        + Copy data from Point{}
        + ...
        '''
        self.record_list.customContextMenuRequested.connect(
            self.on_record_list_context_menu
        )
        self.popMenu_record_list = QMenu(self)
        self.pathData = {}
    
    def clear(self):
        self.pathData.clear()
        for i in range(self.record_list.count() - 1):
            self.record_list.takeItem(1)
        self.variable_list.clear()
    
    @pyqtSlot(tuple)
    def setSelection(self, selections):
        """Set one selection from canvas."""
        self.joint_list.setCurrentRow(
            selections[0]
            if selections[0] in self.Entities_Point.selectedRows()
            else -1
        )
    
    @pyqtSlot()
    def clearSelection(self):
        """Clear the points selection."""
        self.joint_list.setCurrentRow(-1)
    
    @pyqtSlot(int)
    def on_joint_list_currentRowChanged(self, row: int):
        """Change the point row from input widget."""
        self.base_link_list.clear()
        if not row > -1:
            return
        if row not in self.Entities_Point.selectedRows():
            self.Entities_Point.setSelections((row,), False)
        for linkName in self.Entities_Point.item(row, 1).text().split(','):
            if not linkName:
                continue
            self.base_link_list.addItem(linkName)
    
    @pyqtSlot(int)
    def on_base_link_list_currentRowChanged(self, row: int):
        """Set the drive links from base link."""
        self.drive_link_list.clear()
        if not row > -1:
            return
        inputs_point = self.joint_list.currentRow()
        linkNames = self.Entities_Point.item(inputs_point, 1).text().split(',')
        for linkName in linkNames:
            if linkName == self.base_link_list.currentItem().text():
                continue
            self.drive_link_list.addItem(linkName)
    
    @pyqtSlot(int)
    def on_drive_link_list_currentRowChanged(self, row: int):
        """Set enable of 'add variable' button."""
        if not row > -1:
            self.variable_list_add.setEnabled(False)
            return
        typeText = self.joint_list.currentItem().text().split()[0]
        self.variable_list_add.setEnabled(typeText=='[R]')
    
    @pyqtSlot()
    def on_variable_list_add_clicked(self):
        """Add inputs variable from click button."""
        self.__addInputsVariable(
            self.joint_list.currentRow(),
            self.base_link_list.currentItem().text(),
            self.drive_link_list.currentItem().text()
        )
    
    def __addInputsVariable(self,
        point: int,
        base_link: str,
        drive_link: str
    ):
        """Add variable with '->' sign."""
        if not self.DOF() > 0:
            return
        for vlink in self.Entities_Link.data():
            if (vlink.name in {base_link, drive_link}) and (len(vlink.points) < 2):
                return
        name = 'Point{}'.format(point)
        vars = [
            name,
            base_link,
            drive_link,
            "{:.02f}".format(self.__getLinkAngle(point, drive_link))
        ]
        for n, base, drive, a in self.getInputsVariables():
            if {base_link, drive_link} == {base, drive}:
                return
        self.CommandStack.beginMacro("Add variable of {}".format(name))
        self.CommandStack.push(AddVariable(
            '->'.join(vars),
            self.variable_list
        ))
        self.CommandStack.endMacro()
    
    def addInputsVariables(self,
        variables: Tuple[Tuple[int, str, str]]
    ):
        """Add from database."""
        for variable in variables:
            self.__addInputsVariable(*variable)
    
    @pyqtSlot(int)
    def __dialOk(self, p0=None):
        """Set the angle of base link and drive link."""
        row = self.variable_list.currentRow()
        enabled = row > -1
        rotatable = (
            enabled and
            not self.FreeMoveMode.isChecked() and
            self.rightInput()
        )
        self.dial.setEnabled(rotatable)
        self.oldVariableValue = self.dial.value() / 100.
        self.variable_play.setEnabled(rotatable)
        self.variable_speed.setEnabled(rotatable)
        self.dial.setValue(float(
            self.variable_list.currentItem().text().split('->')[-1]
        )*100 if enabled else 0)
    
    def variableExcluding(self, row: int =None):
        """Remove variable if the point was been deleted.
        
        Default: all.
        """
        one_row = row is not None
        for i, variable in enumerate(self.getInputsVariables()):
            row_ = variable[0]
            #If this is not origin point any more.
            if one_row and (row != row_):
                continue
            self.CommandStack.beginMacro("Remove variable of Point{}".format(row))
            self.CommandStack.push(DeleteVariable(i, self.variable_list))
            self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_variable_remove_clicked(self):
        """Remove and reset angle."""
        row = self.variable_list.currentRow()
        if not row > -1:
            return
        reply = QMessageBox.question(self,
            "Remove variable",
            "Do you want to remove this variable?"
        )
        if reply != QMessageBox.Yes:
            return
        self.variable_stop.click()
        self.CommandStack.beginMacro("Remove variable of Point{}".format(row))
        self.CommandStack.push(DeleteVariable(row, self.variable_list))
        self.CommandStack.endMacro()
        self.Entities_Point.getBackPosition()
        self.resolve()
    
    def __getLinkAngle(self, row: int, link: str) -> float:
        """Get the angle of base link and drive link."""
        Point = self.Entities_Point.data()
        Link = self.Entities_Link.data()
        LinkIndex = [vlink.name for vlink in Link]
        relate = Link[LinkIndex.index(link)].points
        base = Point[row]
        drive = Point[relate[relate.index(row)-1]]
        return base.slopeAngle(drive)
    
    def getInputsVariables(self) -> Tuple[int, str, str, float]:
        """A generator use to get variables.
        
        [0]: point num
        [1]: base link
        [2]: drive link
        [3]: angle
        """
        for row in range(self.variable_list.count()):
            variable = self.variable_list.item(row).text().split('->')
            variable[0] = int(variable[0].replace('Point', ''))
            variable[3] = float(variable[3])
            yield tuple(variable)
    
    def inputCount(self) -> int:
        """Use to show input variable count."""
        return self.variable_list.count()
    
    def inputPair(self) -> Tuple[int, int]:
        """Back as point number code."""
        vlinks = {
            vlink.name: set(vlink.points)
            for vlink in self.Entities_Link.data()
        }
        for vars in self.getInputsVariables():
            points = vlinks[vars[2]].copy()
            points.remove(vars[0])
            yield (vars[0], points.pop())
    
    def variableReload(self):
        """Auto check the points and type."""
        self.joint_list.clear()
        for i in range(self.Entities_Point.rowCount()):
            text = "[{}] Point{}".format(
                self.Entities_Point.item(i, 2).text(),
                i
            )
            self.joint_list.addItem(text)
        self.variableValueReset()
    
    def __variableValueUpdate(self, value):
        """Update the value when rotating QDial."""
        item = self.variable_list.currentItem()
        value /= 100.
        if item:
            itemText = item.text().split('->')
            itemText[-1] = "{:.02f}".format(value)
            item.setText('->'.join(itemText))
            self.resolve()
        interval = self.record_interval.value()
        if (
            self.record_start.isChecked() and
            abs(self.oldVariableValue - value) > interval
        ):
            self.DynamicCanvasView.recordPath()
            self.oldVariableValue = value
    
    def variableValueReset(self):
        """Reset the value of QDial."""
        if self.inputs_playShaft.isActive():
            self.variable_play.setChecked(False)
            self.inputs_playShaft.stop()
        self.Entities_Point.getBackPosition()
        for i, variable in enumerate(self.getInputsVariables()):
            point = variable[0]
            text = '->'.join([
                'Point{}'.format(point),
                variable[1],
                variable[2],
                "{:.02f}".format(self.__getLinkAngle(point, variable[2]))
            ])
            self.variable_list.item(i).setText(text)
        self.__dialOk()
        self.resolve()
    
    @pyqtSlot(bool)
    def on_variable_play_toggled(self, toggled):
        """Triggered when play button was changed."""
        self.dial.setEnabled(not toggled)
        if toggled:
            self.inputs_playShaft.start()
        else:
            self.inputs_playShaft.stop()
    
    @pyqtSlot()
    def __changeIndex(self):
        """QTimer change index."""
        index = self.dial.value()
        speed = self.variable_speed.value()
        extremeRebound = (
            self.ConflictGuide.isVisible() and
            self.extremeRebound.isChecked()
        )
        if extremeRebound:
            speed *= -1
            self.variable_speed.setValue(speed)
        index += int(speed * 6 * (3 if extremeRebound else 1))
        index %= self.dial.maximum()
        self.dial.setValue(index)
    
    @pyqtSlot(bool)
    def on_record_start_toggled(self, toggled):
        """Save to file path data."""
        if toggled:
            self.DynamicCanvasView.recordStart(int(
                360 / self.record_interval.value()
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
            self.record_list,
            name,
            self.pathData,
            path
        ))
        self.CommandStack.endMacro()
        self.record_list.setCurrentRow(self.record_list.count() - 1)
    
    def loadPaths(self, paths: Tuple[Tuple[Tuple[float, float]]]):
        """Add multiple path."""
        for name, path in paths.items():
            self.addPath(name, path)
    
    @pyqtSlot()
    def on_record_remove_clicked(self):
        """Remove path data."""
        row = self.record_list.currentRow()
        if not row > 0:
            return
        self.CommandStack.beginMacro("Delete {{Path: {}}}".format(
            self.record_list.item(row).text()
        ))
        self.CommandStack.push(DeletePath(
            row,
            self.record_list,
            self.pathData
        ))
        self.CommandStack.endMacro()
        self.record_list.setCurrentRow(self.record_list.count() - 1)
        self.reloadCanvas()
    
    @pyqtSlot(QListWidgetItem)
    def on_record_list_itemDoubleClicked(self, item):
        """View path data."""
        name = item.text().split(":")[0]
        try:
            data = self.pathData[name]
        except KeyError:
            return
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
    def on_record_list_context_menu(self, point):
        """Show the context menu.
        
        Show path [0], [1], ...
        Or copy path coordinates.
        """
        row = self.record_list.currentRow()
        if row > -1:
            action = self.popMenu_record_list.addAction("Show all")
            action.index = -1
            name = self.record_list.item(row).text().split(":")[0]
            try:
                data = self.pathData[name]
            except KeyError:
                return
            for action_text in ("Show", "Copy data from"):
                self.popMenu_record_list.addSeparator()
                for i in range(len(data)):
                    if data[i]:
                        action = self.popMenu_record_list.addAction(
                            "{} Point{}".format(action_text, i)
                        )
                        action.index = i
        action = self.popMenu_record_list.exec_(
            self.record_list.mapToGlobal(point)
        )
        if action:
            if "Copy data from" in action.text():
                QApplication.clipboard().setText('\n'.join(
                    "{},{}".format(x, y) for x, y in data[action.index]
                ))
            elif "Show" in action.text():
                if action.index==-1:
                    self.record_show.setChecked(True)
                self.DynamicCanvasView.setPathShow(action.index)
        self.popMenu_record_list.clear()
    
    @pyqtSlot()
    def on_record_show_clicked(self):
        """Show all paths or hide."""
        if self.record_show.isChecked():
            show = -1
        else:
            show = -2
        self.DynamicCanvasView.setPathShow(show)
    
    @pyqtSlot(int)
    def on_record_list_currentRowChanged(self, row):
        """Reload the canvas when switch the path."""
        if self.record_show.isChecked():
            self.DynamicCanvasView.setPathShow(-1)
        self.reloadCanvas()
    
    def currentPath(self):
        """Return current path data to main canvas.
        
        + No path.
        + Show path data.
        + Auto preview.
        """
        row = self.record_list.currentRow()
        if row == -1:
            self.DynamicCanvasView.setAutoPath(False)
            return ()
        elif row > 0:
            self.DynamicCanvasView.setAutoPath(False)
            name = self.record_list.item(row).text()
            return self.pathData.get(name.split(':')[0], ())
        elif row == 0:
            self.DynamicCanvasView.setAutoPath(True)
            return ()
