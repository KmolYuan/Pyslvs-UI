# -*- coding: utf-8 -*-

"""The widget of 'Inputs' tab."""

import csv
from typing import (
    Tuple,
    Iterator,
    Optional,
)
from core.QtModules import (
    pyqtSignal,
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
from .rotatable import RotatableView
from .Ui_inputs import Ui_Form


class InputsWidget(QWidget, Ui_Form):
    
    """There has following functions:
    
    + Function of mechanism variables settings.
    + Path recording.
    """
    
    aboutToResolve = pyqtSignal()
    
    def __init__(self, parent: QWidget):
        super(InputsWidget, self).__init__(parent)
        self.setupUi(self)
        #parent's function pointer.
        self.freemode_button = parent.freemode_button
        self.EntitiesPoint = parent.EntitiesPoint
        self.EntitiesLink = parent.EntitiesLink
        self.MainCanvas = parent.MainCanvas
        self.resolve = parent.resolve
        self.reloadCanvas = parent.reloadCanvas
        self.outputTo = parent.outputTo
        self.ConflictGuide = parent.ConflictGuide
        self.DOF = lambda: parent.DOF
        self.rightInput = parent.rightInput
        self.CommandStack = parent.CommandStack
        self.setCoordsAsCurrent = parent.setCoordsAsCurrent
        
        #self widgets.
        self.dial = QDial()
        self.dial.setStatusTip("Input widget of rotatable joint.")
        self.dial.setEnabled(False)
        self.dial.valueChanged.connect(self.__updateVar)
        self.dial_spinbox.valueChanged.connect(self.__setVar)
        self.inputs_dial_layout.addWidget(RotatableView(self.dial))
        
        self.variable_stop.clicked.connect(self.variableValueReset)
        
        self.inputs_playShaft = QTimer(self)
        self.inputs_playShaft.setInterval(10)
        self.inputs_playShaft.timeout.connect(self.__changeIndex)
        
        self.variable_list.currentRowChanged.connect(self.__dialOk)
        self.update_pos.clicked.connect(self.setCoordsAsCurrent)
        
        """Inputs record context menu
        
        + Copy data from Point{}
        + ...
        """
        self.popMenu_record_list = QMenu(self)
        self.record_list.customContextMenuRequested.connect(
            self.on_record_list_context_menu
        )
        self.pathData = {}
    
    def clear(self):
        self.pathData.clear()
        for i in range(self.record_list.count() - 1):
            self.record_list.takeItem(1)
        self.variable_list.clear()
    
    @pyqtSlot(tuple)
    def setSelection(self, selections: Tuple[int]):
        """Set one selection from canvas."""
        self.joint_list.setCurrentRow(selections[0])
    
    @pyqtSlot()
    def clearSelection(self):
        """Clear the points selection."""
        self.driver_list.clear()
        self.joint_list.setCurrentRow(-1)
    
    @pyqtSlot(int)
    def on_joint_list_currentRowChanged(self, p0: int):
        """Change the point row from input widget."""
        self.driver_list.clear()
        if not p0 > -1:
            return
        if p0 not in self.EntitiesPoint.selectedRows():
            self.EntitiesPoint.setSelections((p0,), False)
        for i, vpoint in enumerate(self.EntitiesPoint.data()):
            self.driver_list.addItem("[{}] Point{}".format(vpoint.typeSTR, i))
    
    @pyqtSlot(int)
    def on_driver_list_currentRowChanged(self, p1: int):
        """Set enable of 'add variable' button."""
        if not p1 > -1:
            self.variable_list_add.setEnabled(False)
            return
        p0 = self.joint_list.currentRow()
        vpoints = self.EntitiesPoint.dataTuple()
        self.variable_list_add.setEnabled(
            p1 != p0 and vpoints[p0].type == 0
        )
    
    @pyqtSlot()
    def on_variable_list_add_clicked(self):
        """Add inputs variable from click button."""
        self.__addInputsVariable(
            self.joint_list.currentRow(),
            self.driver_list.currentRow()
        )
    
    def __addInputsVariable(self, p0: int, p1: int):
        """Add variable with '->' sign."""
        if self.DOF() <= 0:
            return
        vpoints = self.EntitiesPoint.dataTuple()
        name = 'Point{}'.format(p0)
        vars = [
            name,
            'Point{}'.format(p1),
            "{:.02f}".format(vpoints[p0].slope_angle(vpoints[p1]))
        ]
        for p0_, p1_, a in self.inputPair():
            if {p0, p1} == {p0_, p1_}:
                return
        self.CommandStack.beginMacro("Add variable of {}".format(name))
        self.CommandStack.push(AddVariable(
            '->'.join(vars),
            self.variable_list
        ))
        self.CommandStack.endMacro()
    
    def addInputsVariables(self, variables: Tuple[Tuple[int, int]]):
        """Add from database."""
        for p0, p1 in variables:
            self.__addInputsVariable(p0, p1)
    
    @pyqtSlot(int)
    def __dialOk(self, p0: Optional[int] = None):
        """Set the angle of base link and drive link."""
        row = self.variable_list.currentRow()
        enabled = row > -1
        rotatable = (
            enabled and
            not self.freemode_button.isChecked() and
            self.rightInput()
        )
        self.dial.setEnabled(rotatable)
        self.dial_spinbox.setEnabled(rotatable)
        self.oldVar = self.dial.value() / 100.
        self.variable_play.setEnabled(rotatable)
        self.variable_speed.setEnabled(rotatable)
        self.dial.setValue(float(
            self.variable_list.currentItem().text().split('->')[-1]
        ) * 100 if enabled else 0)
    
    def variableExcluding(self, row: int = None):
        """Remove variable if the point was been deleted.
        
        Default: all.
        """
        one_row = row is not None
        for i, variable in enumerate(self.inputPair()):
            #If this is not origin point any more.
            if one_row and (row != variable[0]):
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
        self.EntitiesPoint.getBackPosition()
        self.resolve()
    
    def inputCount(self) -> int:
        """Use to show input variable count."""
        return self.variable_list.count()
    
    def inputPair(self) -> Iterator[Tuple[int, int, float]]:
        """Back as point number code."""
        for row in range(self.variable_list.count()):
            vars = self.variable_list.item(row).text().split('->')
            yield (
                int(vars[0].replace('Point', '')),
                int(vars[1].replace('Point', '')),
                float(vars[2]),
            )
    
    def variableReload(self):
        """Auto check the points and type."""
        self.joint_list.clear()
        for i in range(self.EntitiesPoint.rowCount()):
            self.joint_list.addItem("[{}] Point{}".format(
                self.EntitiesPoint.item(i, 2).text(),
                i
            ))
        self.variableValueReset()
    
    @pyqtSlot(float)
    def __setVar(self, value):
        self.dial.setValue(int(value % 360 * 100))
    
    @pyqtSlot(int)
    def __updateVar(self, value):
        """Update the value when rotating QDial."""
        item = self.variable_list.currentItem()
        value /= 100.
        self.dial_spinbox.blockSignals(True)
        self.dial_spinbox.setValue(value)
        self.dial_spinbox.blockSignals(False)
        if item:
            itemText = item.text().split('->')
            itemText[-1] = "{:.02f}".format(value)
            item.setText('->'.join(itemText))
            self.aboutToResolve.emit()
        if (
            self.record_start.isChecked() and
            abs(self.oldVar - value) > self.record_interval.value()
        ):
            self.MainCanvas.recordPath()
            self.oldVar = value
    
    def variableValueReset(self):
        """Reset the value of QDial."""
        if self.inputs_playShaft.isActive():
            self.variable_play.setChecked(False)
            self.inputs_playShaft.stop()
        self.EntitiesPoint.getBackPosition()
        vpoints = self.EntitiesPoint.dataTuple()
        for i, (p0, p1, a) in enumerate(self.inputPair()):
            self.variable_list.item(i).setText('->'.join([
                'Point{}'.format(p0),
                'Point{}'.format(p1),
                "{:.02f}".format(vpoints[p0].slope_angle(vpoints[p1]))
            ]))
        self.__dialOk()
        self.resolve()
    
    @pyqtSlot(bool)
    def on_variable_play_toggled(self, toggled):
        """Triggered when play button was changed."""
        self.dial.setEnabled(not toggled)
        self.dial_spinbox.setEnabled(not toggled)
        if toggled:
            self.inputs_playShaft.start()
        else:
            self.inputs_playShaft.stop()
            if self.update_pos_option.isChecked():
                self.setCoordsAsCurrent()
    
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
            self.MainCanvas.recordStart(int(360 / self.record_interval.value()))
            return
        path = self.MainCanvas.getRecordPath()
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
        file_name = self.outputTo(
            "path data",
            ["Comma-Separated Values (*.csv)", "Text file (*.txt)"]
        )
        if not file_name:
            return
        with open(file_name, 'w', newline='') as stream:
            writer = csv.writer(stream)
            for point in data:
                for coordinate in point:
                    writer.writerow(coordinate)
                writer.writerow(())
        print("Output path data: {}".format(file_name))
    
    @pyqtSlot(QPoint)
    def on_record_list_context_menu(self, point):
        """Show the context menu.
        
        Show path [0], [1], ...
        Or copy path coordinates.
        """
        row = self.record_list.currentRow()
        if not row > -1:
            return
        showall_action = self.popMenu_record_list.addAction("Show all")
        showall_action.index = -1
        copy_action = self.popMenu_record_list.addAction("Copy as new")
        name = self.record_list.item(row).text().split(":")[0]
        try:
            data = self.pathData[name]
        except KeyError:
            #Auto preview path.
            data = self.MainCanvas.Path.path
            showall_action.setEnabled(False)
        else:
            for action_text in ("Show", "Copy data from"):
                self.popMenu_record_list.addSeparator()
                for i in range(len(data)):
                    if data[i]:
                        action = self.popMenu_record_list.addAction(
                            "{} Point{}".format(action_text, i)
                        )
                        action.index = i
        action_exec = self.popMenu_record_list.exec_(
            self.record_list.mapToGlobal(point)
        )
        if action_exec:
            if action_exec == copy_action:
                """Copy path data."""
                num = 0
                while "Copied_{}".format(num) in self.pathData:
                    num += 1
                self.addPath("Copied_{}".format(num), data)
            elif "Copy data from" in action_exec.text():
                """Copy data to clipboard."""
                QApplication.clipboard().setText('\n'.join(
                    "{},{}".format(x, y) for x, y in data[action_exec.index]
                ))
            elif "Show" in action_exec.text():
                """Switch points enabled status."""
                if action_exec.index == -1:
                    self.record_show.setChecked(True)
                self.MainCanvas.setPathShow(action_exec.index)
        self.popMenu_record_list.clear()
    
    @pyqtSlot()
    def on_record_show_clicked(self):
        """Show all paths or hide."""
        if self.record_show.isChecked():
            show = -1
        else:
            show = -2
        self.MainCanvas.setPathShow(show)
    
    @pyqtSlot(int)
    def on_record_list_currentRowChanged(self, row):
        """Reload the canvas when switch the path."""
        if self.record_show.isChecked():
            self.MainCanvas.setPathShow(-1)
        self.reloadCanvas()
    
    def currentPath(self):
        """Return current path data to main canvas.
        
        + No path.
        + Show path data.
        + Auto preview.
        """
        row = self.record_list.currentRow()
        if row == -1:
            self.MainCanvas.setAutoPath(False)
            return ()
        elif row > 0:
            self.MainCanvas.setAutoPath(False)
            name = self.record_list.item(row).text()
            return self.pathData.get(name.split(':')[0], ())
        elif row == 0:
            self.MainCanvas.setAutoPath(True)
            return ()
