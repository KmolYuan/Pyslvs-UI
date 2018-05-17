# -*- coding: utf-8 -*-

"""The widget of 'Dimensional synthesis' tab."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from networkx import Graph
import csv
import openpyxl
import pprint
from copy import deepcopy
from re import split as charSplit
from typing import (
    List,
    Dict,
    Tuple,
    Any,
    Optional,
)
from core.QtModules import (
    pyqtSlot,
    QWidget,
    QApplication,
    QMessageBox,
    QListWidgetItem,
    QIcon,
    QPixmap,
    QModelIndex,
    QInputDialog,
    QDoubleSpinBox,
    QTableWidgetItem,
)
from core.graphics import (
    PreviewCanvas,
    graph2vpoints,
)
from core.io import (
    strbetween,
    strbefore,
)
from core.libs import expr_path
from core.synthesis import CollectionsDialog
from .DimensionalSynthesis_dialog import (
    GeneticPrams,
    FireflyPrams,
    defaultSettings,
    DifferentialPrams,
    AlgorithmType,
    Options_show,
    PathAdjustDialog,
    ProgressDialog,
    PreviewDialog,
    ChartDialog,
)
from .Ui_Algorithm import Ui_Form


class DimensionalSynthesis(QWidget, Ui_Form):
    
    """Dimensional synthesis widget.
    
    User can run the dimensional synthesis here.
    """
    
    def __init__(self, parent):
        """Reference names:
        
        + Iteration collections.
        + Result data.
        + Main window function references.
        """
        super(DimensionalSynthesis, self).__init__(parent)
        self.setupUi(self)
        
        self.mech_params = {}
        self.path = {}
        
        #Some reference of 'collections'.
        self.collections = parent.CollectionTabPage.TriangularIterationWidget.collections
        self.getCollection = parent.getCollection
        self.inputFrom = parent.inputFrom
        self.unsaveFunc = parent.workbookNoSave
        self.mergeResult = parent.mergeResult
        self.updateRanges = parent.MainCanvas.updateRanges
        self.setSolvingPath = parent.MainCanvas.setSolvingPath
        
        #Data and functions.
        self.mechanism_data = []
        self.Settings = deepcopy(defaultSettings)
        self.__setAlgorithmToDefault()
        
        def get_solutions_func():
            """For preview canvas."""
            try:
                return self.mech_params['Expression']
            except KeyError:
                return ()
        
        self.PreviewCanvas = PreviewCanvas(get_solutions_func, self)
        self.preview_layout.addWidget(self.PreviewCanvas)
        self.show_solutions.clicked.connect(self.PreviewCanvas.setShowSolutions)
        
        #Splitter
        self.up_splitter.setSizes([80, 100])
        
        #Table widget column width.
        self.ground_joints.setColumnWidth(0, 50)
        self.ground_joints.setColumnWidth(1, 80)
        self.ground_joints.setColumnWidth(2, 70)
        self.ground_joints.setColumnWidth(3, 70)
        self.ground_joints.setColumnWidth(4, 80)
        
        #Default value of algorithm parameters.
        self.type0.clicked.connect(self.__setAlgorithmToDefault)
        self.type1.clicked.connect(self.__setAlgorithmToDefault)
        self.type2.clicked.connect(self.__setAlgorithmToDefault)
        
        #Signals
        self.Result_list.clicked.connect(self.__hasResult)
        self.path_clear.clicked.connect(self.__clearPath)
    
    def clear(self):
        """Clear all sub-widgets."""
        self.mechanism_data.clear()
        self.Result_list.clear()
        self.__clearSettings()
        self.__hasResult()
    
    def __clearSettings(self):
        """Clear sub-widgets that contain the setting."""
        self.__clearPath(ask=False)
        self.path.clear()
        self.mech_params.clear()
        self.PreviewCanvas.clear()
        self.Settings.clear()
        self.Settings = deepcopy(defaultSettings)
        self.profile_name.setText("No setting")
        self.type2.setChecked(True)
        self.ground_joints.setRowCount(0)
        self.target_points.clear()
        self.Expression.clear()
        self.Link_Expression.clear()
        self.updateRange()
        self.__ableToGenerate()
    
    def on_clear_button_clicked(self):
        if self.profile_name.text() == "No setting":
            return
        reply = QMessageBox.question(
            self,
            "Clear setting",
            "Do you want to clear the setting?"
        )
        if reply == QMessageBox.Yes:
            self.__clearSettings()
    
    def loadResults(self,
        mechanism_data: List[Dict[str, Any]]
    ):
        """Append results of workbook database to memory."""
        for e in mechanism_data:
            self.mechanism_data.append(e)
            self.__addResult(e)
    
    def __currentPathChanged(self):
        """Call the canvas to update to current target path."""
        self.setSolvingPath({
            name: tuple(path) for name, path in self.path.items()
        })
        self.__ableToGenerate()
    
    def currentPath(self) -> List[Tuple[float, float]]:
        """Return the pointer of current target path."""
        item = self.target_points.currentItem()
        if item:
            return self.path[item.text()]
        else:
            return []
    
    @pyqtSlot(str)
    def on_target_points_currentTextChanged(self, text: Optional[str] = None):
        """Switch to the current target path."""
        self.path_list.clear()
        for x, y in self.currentPath():
            self.path_list.addItem("({:.04f}, {:.04f})".format(x, y))
        self.__currentPathChanged()
    
    @pyqtSlot()
    def __clearPath(self, *, ask: bool = True):
        """Clear the current target path."""
        if ask:
            reply = QMessageBox.question(self,
                "Clear path",
                "Are you sure to clear the current path?"
            )
            if reply != QMessageBox.Yes:
                return
        self.currentPath().clear()
        self.path_list.clear()
        self.__currentPathChanged()
    
    @pyqtSlot()
    def on_path_copy_clicked(self):
        """Copy the current path coordinates to clipboard."""
        QApplication.clipboard().setText('\n'.join(
            "{},{}".format(x, y)
            for x, y in self.currentPath()
        ))
    
    @pyqtSlot()
    def on_path_paste_clicked(self):
        """Paste path data from clipboard."""
        self.__readPathFromCSV(charSplit(";|,|\n", QApplication.clipboard().text()))
    
    @pyqtSlot()
    def on_importCSV_clicked(self):
        """Paste path data from a text file."""
        file_name = self.inputFrom(
            "Path data",
            ["Text file (*.txt)",
            "Comma-Separated Values (*.csv)"]
        )
        if not file_name:
            return
        data = []
        with open(file_name, newline='') as stream:
            reader = csv.reader(stream, delimiter=' ', quotechar='|')
            for row in reader:
                data += ' '.join(row).split(',')
        self.__readPathFromCSV(data)
    
    def __readPathFromCSV(self, data: List[str]):
        """Trun STR to FLOAT then add them to current target path."""
        try:
            data = [
                (round(float(data[i]), 4), round(float(data[i + 1]), 4))
                for i in range(0, len(data), 2)
            ]
        except:
            QMessageBox.warning(self, "File error",
                "Wrong format.\nIt should be look like this:" +
                "\n0.0,0.0[\\n]" * 3
            )
        else:
            for e in data:
                self.addPoint(e[0], e[1])
    
    @pyqtSlot()
    def on_importXLSX_clicked(self):
        """Paste path data from a Excel file."""
        file_name = self.inputFrom(
            "Excel file",
            ["Microsoft Office Excel (*.xlsx *.xlsm *.xltx *.xltm)"]
        )
        if not file_name:
            return
        wb = openpyxl.load_workbook(file_name)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        data = []
        #Keep finding until there is no value.
        i = 1
        while True:
            x = ws.cell(row=i, column=1).value
            y = ws.cell(row=i, column=2).value
            if x == None or y == None:
                break
            try:
                data.append((round(float(x), 4), round(float(y), 4)))
            except:
                QMessageBox.warning(self,
                    "File error",
                    "Wrong format.\n" +
                    "The datasheet seems to including non-digital cell."
                )
                break
            i += 1
        for x, y in data:
            self.addPoint(x, y)
    
    @pyqtSlot()
    def on_pathAdjust_clicked(self):
        """Show up path adjust dialog and
        get back the changes of current target path.
        """
        dlg = PathAdjustDialog(self)
        dlg.show()
        if not dlg.exec_():
            return
        self.__clearPath(ask=False)
        for e in dlg.r_path:
            self.addPoint(e[0], e[1])
        self.__currentPathChanged()
    
    def addPoint(self, x: float, y: float):
        """Add path data to list widget and
        current target path.
        """
        x = round(x, 4)
        y = round(y, 4)
        self.currentPath().append((x, y))
        self.path_list.addItem("({:.04f}, {:.04f})".format(x, y))
        self.__currentPathChanged()
    
    @pyqtSlot()
    def on_close_path_clicked(self):
        """Add a the last point same as first point."""
        currentPath = self.currentPath()
        if (self.path_list.count() > 1) and (currentPath[0] != currentPath[-1]):
            self.addPoint(*currentPath[0])
    
    @pyqtSlot()
    def on_point_up_clicked(self):
        """Target point move up."""
        row = self.path_list.currentRow()
        if not ((row > 0) and (self.path_list.count() > 1)):
            return
        path = self.currentPath()
        path.insert(row - 1, (path[row][0], path[row][1]))
        del path[row + 1]
        x, y = self.path_list.currentItem().text()[1:-1].split(", ")
        self.path_list.insertItem(row - 1, "({}, {})".format(x, y))
        self.path_list.takeItem(row + 1)
        self.path_list.setCurrentRow(row - 1)
        self.__currentPathChanged()
    
    @pyqtSlot()
    def on_point_down_clicked(self):
        """Target point move down."""
        row = self.path_list.currentRow()
        if not (
            (row < self.path_list.count() - 1) and
            (self.path_list.count() > 1)
        ):
            return
        path = self.currentPath()
        path.insert(row + 2, (path[row][0], path[row][1]))
        del path[row]
        x, y = self.path_list.currentItem().text()[1:-1].split(", ")
        self.path_list.insertItem(row+2, "({}, {})".format(x, y))
        self.path_list.takeItem(row)
        self.path_list.setCurrentRow(row+1)
        self.__currentPathChanged()
    
    @pyqtSlot()
    def on_point_delete_clicked(self):
        """Delete a target point."""
        row = self.path_list.currentRow()
        if not row > -1:
            return
        del self.currentPath()[row]
        self.path_list.takeItem(row)
        self.__currentPathChanged()
    
    def __ableToGenerate(self):
        """Set button enable if all the data are already."""
        self.pointNum.setText(
            "<p><span style=\"font-size:12pt; color:#00aa00;\">{}</span></p>"
            .format(self.path_list.count())
        )
        n = (
            bool(self.mech_params) and
            (self.path_list.count() > 1) and
            bool(self.Expression.text())
        )
        self.pathAdjust.setEnabled(n)
        self.generate_button.setEnabled(n)
    
    @pyqtSlot()
    def on_generate_button_clicked(self):
        """Start synthesis."""
        #Check if the number of target points are same.
        leng = -1
        for path in self.path.values():
            if leng<0:
                leng = len(path)
            if len(path)!=leng:
                QMessageBox.warning(self, "Target Error",
                    "The length of target paths should be the same."
                )
                return
        #Get the algorithm type.
        if self.type0.isChecked():
            type_num = AlgorithmType.RGA
        elif self.type1.isChecked():
            type_num = AlgorithmType.Firefly
        elif self.type2.isChecked():
            type_num = AlgorithmType.DE
        #Deep copy it so the pointer will not the same.
        mech_params = deepcopy(self.mech_params)
        mech_params['Target'] = deepcopy(self.path)
        
        def name_in_table(name: str) -> int:
            """Find a name and return the row from the table."""
            for row in range(self.ground_joints.rowCount()):
                if self.ground_joints.item(row, 0).text() == name:
                    return row
        
        for key in ('Driver', 'Follower'):
            for name in mech_params[key]:
                row = name_in_table(name)
                mech_params[key][name] = (
                    self.ground_joints.cellWidget(row, 2).value(),
                    self.ground_joints.cellWidget(row, 3).value(),
                    self.ground_joints.cellWidget(row, 4).value()
                )
        for name in ['IMax', 'IMin', 'LMax', 'LMin', 'FMax', 'FMin', 'AMax', 'AMin']:
            mech_params[name] = self.Settings[name]
        setting = {'report': self.Settings['report']}
        if 'maxGen' in self.Settings:
            setting['maxGen'] = self.Settings['maxGen']
        elif 'minFit' in self.Settings:
            setting['minFit'] = self.Settings['minFit']
        elif 'maxTime' in self.Settings:
            setting['maxTime'] = self.Settings['maxTime']
        setting.update(self.Settings['algorithmPrams'])
        #Start progress dialog.
        dlg = ProgressDialog(
            type_num,
            mech_params,
            setting,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        for m in dlg.mechanisms:
            self.mechanism_data.append(m)
            self.__addResult(m)
        self.__setTime(dlg.time_spand)
        self.unsaveFunc()
        QMessageBox.information(self,
            "Dimensional Synthesis",
            "Your tasks is all completed.",
            QMessageBox.Ok
        )
        print("Finished.")
    
    def __setTime(self, time: float):
        """Set the time label."""
        self.timeShow.setText(
            "<html><head/><body><p><span style=\"font-size:16pt\">" +
            "{}[min] {:.02f}[s]".format(int(time // 60), time % 60) +
            "</span></p></body></html>"
        )
    
    def __addResult(self, result: Dict[str, Any]):
        """Add result items, except add to the list."""
        item = QListWidgetItem(result['Algorithm'])
        interrupt = result['interrupted']
        if interrupt=='False':
            item.setIcon(QIcon(QPixmap(":/icons/task-completed.png")))
        elif interrupt=='N/A':
            item.setIcon(QIcon(QPixmap(":/icons/question-mark.png")))
        else:
            item.setIcon(QIcon(QPixmap(":/icons/interrupted.png")))
        text = "{} ({})".format(
            result['Algorithm'],
            "No interrupt." if interrupt=='False' else "Interrupt at {}".format(interrupt)
        )
        if interrupt == 'N/A':
            text += "\n※Completeness is not clear."
        item.setToolTip(text)
        self.Result_list.addItem(item)
    
    @pyqtSlot()
    def on_deleteButton_clicked(self):
        """Delete a result."""
        row = self.Result_list.currentRow()
        if not row>-1:
            return
        reply = QMessageBox.question(self,
            "Delete",
            "Delete this result from list?"
        )
        if reply != QMessageBox.Yes:
            return
        del self.mechanism_data[row]
        self.Result_list.takeItem(row)
        self.unsaveFunc()
        self.__hasResult()
    
    @pyqtSlot()
    def __hasResult(self):
        """Set enable if there has any result."""
        for button in [
            self.mergeButton,
            self.deleteButton,
            self.Result_load_settings,
            self.Result_chart,
            self.Result_clipboard
        ]:
            button.setEnabled(self.Result_list.currentRow()>-1)
    
    @pyqtSlot(QModelIndex)
    def on_Result_list_doubleClicked(self, index):
        """Double click result item can show up preview dialog."""
        row = self.Result_list.currentRow()
        if not row>-1:
            return
        dlg = PreviewDialog(self.mechanism_data[row], self.__getPath(row), self)
        dlg.show()
        dlg.exec_()
    
    @pyqtSlot()
    def on_mergeButton_clicked(self):
        """Merge mechanism into main canvas."""
        row = self.Result_list.currentRow()
        if not row>-1:
            return
        reply = QMessageBox.question(self,
            "Merge",
            "Merge this result to your canvas?"
        )
        if reply == QMessageBox.Yes:
            self.mergeResult(row, self.__getPath(row))
    
    def __getPath(self, row: int):
        """Using result data to generate paths of mechanism."""
        Result = self.mechanism_data[row]
        point_index = sorted(
            int(tag.replace('P', ''))
            for tag in Result if tag.replace('P', '').isdigit()
        )
        exprs = []
        for expr in Result['Expression'].split(';'):
            func = strbefore(expr, '[')
            params = strbetween(expr, '[', ']').split(',')
            target = strbetween(expr, '(', ')')
            params.insert(0, func)
            params.append(target)
            exprs.append(tuple(params))
        pos = {}
        for name in Result['pos']:
            try:
                pos[name] = Result['P{}'.format(name)]
            except KeyError:
                pos[name] = Result['pos'][name]
        vpoints = graph2vpoints(
            Graph(Result['Graph']),
            pos,
            Result['cus'],
            Result['same']
        )
        return [path for i, path in enumerate(expr_path(
            tuple(exprs),
            {n: 'P{}'.format(n) for n in range(len(vpoints))},
            vpoints,
            3
        )) if (i in point_index)]
    
    @pyqtSlot()
    def on_Result_chart_clicked(self):
        """Show up the chart dialog."""
        dlg = ChartDialog("Convergence Value", self.mechanism_data, self)
        dlg.show()
        dlg.exec_()
    
    @pyqtSlot()
    def on_Result_clipboard_clicked(self):
        """Copy pretty print result as text."""
        QApplication.clipboard().setText(
            pprint.pformat(self.mechanism_data[self.Result_list.currentRow()])
        )
    
    @pyqtSlot()
    def on_save_button_clicked(self):
        """Save as new profile to collection widget."""
        if not self.mech_params:
            return
        name, ok = QInputDialog.getText(self,
            "Profile name",
            "Please enter the profile name:"
        )
        if not ok:
            return
        i = 0
        while (name not in self.collections) and (not name):
            name = "Structure_{}".format(i)
        mech_params = deepcopy(self.mech_params)
        for key in [
            'Driver',
            'Follower',
            'Target'
        ]:
            for name in mech_params[key]:
                mech_params[key][name] = None
        self.collections[name] = mech_params
        self.unsaveFunc()
    
    @pyqtSlot()
    def on_load_profile_clicked(self):
        """Load profile from collections dialog."""
        dlg = CollectionsDialog(
            self.collections,
            self.getCollection,
            self
        )
        dlg.show()
        if dlg.exec_():
            self.__setProfile(dlg.name(), dlg.params())
    
    def __setProfile(self, profile_name: str, params: Dict[str, Any]):
        """Set profile to sub-widgets."""
        self.__clearSettings()
        self.profile_name.setText(profile_name)
        self.Expression.setText(params['Expression'])
        self.Link_Expression.setText(params['Link_Expression'])
        for name in sorted(params['Target']):
            self.target_points.addItem(name)
            path = params['Target'][name]
            if path:
                self.path[name] = path.copy()
            else:
                self.path[name] = []
        if self.target_points.count():
            self.target_points.setCurrentRow(0)
        gj = {}
        for key in ('Driver', 'Follower'):
            gj.update(params[key])
        self.ground_joints.setRowCount(0)
        self.ground_joints.setRowCount(len(gj))
        
        def spinbox(v: float, prefix: bool = False):
            s = QDoubleSpinBox(self)
            s.setMinimum(-1000000.0)
            s.setMaximum(1000000.0)
            s.setSingleStep(10.0)
            s.setValue(v)
            if prefix:
                s.setPrefix("±")
            return s
        
        for row, name in enumerate(sorted(gj)):
            coord = gj[name]
            self.ground_joints.setItem(row, 0, QTableWidgetItem(name))
            if name in params['Driver']:
                role = 'Driver'
            else:
                role = 'Follower'
            self.ground_joints.setItem(row, 1, QTableWidgetItem(role))
            x, y = params['pos'][int(name.replace('P', ''))]
            s1 = spinbox(coord[0] if coord else x)
            s2 = spinbox(coord[1] if coord else y)
            s3 = spinbox(coord[2] if coord else 50., True)
            self.ground_joints.setCellWidget(row, 2, s1)
            self.ground_joints.setCellWidget(row, 3, s2)
            self.ground_joints.setCellWidget(row, 4, s3)
            for s in (s1, s2, s3):
                s.valueChanged.connect(self.updateRange)
        self.PreviewCanvas.from_profile(params)
        self.mech_params = params
        self.updateRange()
        self.__ableToGenerate()
        if not self.Expression.text():
            QMessageBox.warning(self,
                "Profile cannot use",
                "This profile has no any solutions, " +
                "you can set it in the \"Triangular iteration\" page."
            )
    
    @pyqtSlot()
    def on_Result_load_settings_clicked(self):
        """Load settings from a result."""
        self.__hasResult()
        row = self.Result_list.currentRow()
        if not row > -1:
            return
        self.__clearSettings()
        Result = self.mechanism_data[row]
        if Result['Algorithm'] == str(AlgorithmType.RGA):
            self.type0.setChecked(True)
        elif Result['Algorithm'] == str(AlgorithmType.Firefly):
            self.type1.setChecked(True)
        elif Result['Algorithm'] == str(AlgorithmType.DE):
            self.type2.setChecked(True)
        #Copy to mechanism params.
        mech_params = {
            'Expression': Result['Expression'],
            'Link_Expression': Result['Link_Expression'],
        }
        for key in [
            'Driver',
            'Follower',
            'Target'
        ]:
            mech_params[key] = Result[key].copy()
        for key in [
            'Link_Expression',
            'Expression',
            'constraint',
            'Graph',
            'pos',
            'cus',
            'same'
        ]:
            mech_params[key] = Result[key]
        self.__setProfile("External setting", mech_params)
        self.__setTime(Result['time'])
        #Load settings.
        settings = Result['settings']
        self.Settings = {
            'report': settings['report'],
            'IMax': Result['IMax'], 'IMin': Result['IMin'],
            'LMax': Result['LMax'], 'LMin': Result['LMin'],
            'FMax': Result['FMax'], 'FMin': Result['FMin'],
            'AMax': Result['AMax'], 'AMin': Result['AMin'],
        }
        if 'maxGen' in settings:
            self.Settings['maxGen'] = settings['maxGen']
        elif 'minFit' in settings:
            self.Settings['minFit'] = settings['minFit']
        elif 'maxTime' in settings:
            self.Settings['maxTime'] = settings['maxTime']
        algorithmPrams = settings.copy()
        del algorithmPrams['report']
        self.Settings['algorithmPrams'] = algorithmPrams
    
    def __setAlgorithmToDefault(self):
        """Set the algorithm settings to default."""
        if self.type0.isChecked():
            self.Settings['algorithmPrams'] = GeneticPrams.copy()
        elif self.type1.isChecked():
            self.Settings['algorithmPrams'] = FireflyPrams.copy()
        elif self.type2.isChecked():
            self.Settings['algorithmPrams'] = DifferentialPrams.copy()
    
    @pyqtSlot()
    def on_advanceButton_clicked(self):
        """Get the settings from advance dialog."""
        if self.type0.isChecked():
            type_num = AlgorithmType.RGA
        elif self.type1.isChecked():
            type_num = AlgorithmType.Firefly
        elif self.type2.isChecked():
            type_num = AlgorithmType.DE
        dlg = Options_show(type_num, self.Settings)
        dlg.show()
        if not dlg.exec_():
            return
        tablePL = lambda row: dlg.PLTable.cellWidget(row, 1).value()
        self.Settings = {
            'report': dlg.report.value(),
            'IMax': tablePL(0), 'IMin': tablePL(1),
            'LMax': tablePL(2), 'LMin': tablePL(3),
            'FMax': tablePL(4), 'FMin': tablePL(5),
            'AMax': tablePL(6), 'AMin': tablePL(7)
        }
        if dlg.maxGen_option.isChecked():
            self.Settings['maxGen'] = dlg.maxGen.value()
        elif dlg.minFit_option.isChecked():
            self.Settings['minFit'] = dlg.minFit.value()
        elif dlg.maxTime_option.isChecked():
            #Three spinbox value translate to second.
            self.Settings['maxTime'] = (
                dlg.maxTime_h.value() * 3600 +
                dlg.maxTime_m.value() * 60 +
                dlg.maxTime_s.value()
            )
        tableAP = lambda row: dlg.APTable.cellWidget(row, 1).value()
        popSize = dlg.popSize.value()
        if type_num == AlgorithmType.RGA:
            self.Settings['algorithmPrams'] = {
                'nPop': popSize,
                'pCross': tableAP(0),
                'pMute': tableAP(1),
                'pWin': tableAP(2),
                'bDelta': tableAP(3)
            }
        elif type_num == AlgorithmType.Firefly:
            self.Settings['algorithmPrams'] = {
                'n': popSize,
                'alpha': tableAP(0),
                'betaMin': tableAP(1),
                'gamma': tableAP(2),
                'beta0': tableAP(3)
            }
        elif type_num == AlgorithmType.DE:
            self.Settings['algorithmPrams'] = {
                'NP': popSize,
                'strategy': tableAP(0),
                'F': tableAP(1),
                'CR': tableAP(2)
            }
    
    @pyqtSlot(float)
    def updateRange(self, p0: Optional[float] = None):
        """Update range values to main canvas."""
        
        def t(x, y):
            item = self.ground_joints.item(x, y)
            if item:
                return item.text()
            else:
                return self.ground_joints.cellWidget(x, y).value()
        
        self.updateRanges({
            t(row, 0): (t(row, 2), t(row, 3), t(row, 4))
            for row in range(self.ground_joints.rowCount())
        })
    
    @pyqtSlot()
    def on_Expression_copy_clicked(self):
        """Copy profile expression."""
        text = self.Expression.text()
        if text:
            QApplication.clipboard().setText(text)
    
    @pyqtSlot()
    def on_Link_Expression_copy_clicked(self):
        """Copy profile linkage expression."""
        text = self.Link_Expression.text()
        if text:
            QApplication.clipboard().setText(text)
