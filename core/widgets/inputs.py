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
        self.drive_link_list.clear()
        self.base_link_list.clear()
        self.joint_list.setCurrentRow(-1)
    
    @pyqtSlot(int)
    def on_joint_list_currentRowChanged(self, row: int):
        """Change the point row from input widget."""
        self.base_link_list.clear()
        if not row > -1:
            return
        if row not in self.EntitiesPoint.selectedRows():
            self.EntitiesPoint.setSelections((row,), False)
        for linkName in self.EntitiesPoint.item(row, 1).text().split(','):
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
        linkNames = self.EntitiesPoint.item(inputs_point, 1).text().split(',')
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
        for vlink in self.EntitiesLink.data():
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
        self.EntitiesPoint.getBackPosition()
        self.resolve()
    
    def __getLinkAngle(self, row: int, linkname: str) -> float:
        """Get the angle of base link and drive link."""
        vpoints = self.EntitiesPoint.dataTuple()
        vlinks = self.EntitiesLink.dataTuple()
        
        def findpoints(name: str) -> Tuple[int]:
            for vlink in vlinks:
                if name == vlink.name:
                    return vlink.points
        
        relate = findpoints(linkname)
        base = vpoints[row]
        drive = vpoints[relate[relate.index(row)-1]]
        return base.slopeAngle(drive)
    
    def getInputsVariables(self) -> Iterator[Tuple[int, str, str, float]]:
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
    
    def inputPair(self) -> Iterator[Tuple[int, int]]:
        """Back as point number code."""
        vlinks = {
            vlink.name: set(vlink.points)
            for vlink in self.EntitiesLink.data()
        }
        for vars in self.getInputsVariables():
            points = vlinks[vars[2]].copy()
            points.remove(vars[0])
            yield (vars[0], points.pop())
    
    def variableReload(self):
        """Auto check the points and type."""
        self.joint_list.clear()
        for i in range(self.EntitiesPoint.rowCount()):
            text = "[{}] Point{}".format(
                self.EntitiesPoint.item(i, 2).text(),
                i
            )
            self.joint_list.addItem(text)
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
            self.MainCanvas.recordStart(int(
                360 / self.record_interval.value()
            ))
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
