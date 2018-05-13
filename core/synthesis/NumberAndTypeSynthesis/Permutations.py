# -*- coding: utf-8 -*-

"""The widget of 'Number and type synthesis' tab."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from networkx import Graph
from typing import List, Optional
from core.QtModules import (
    QWidget,
    QMenu,
    QAction,
    QIcon,
    QPixmap,
    pyqtSlot,
    QListWidgetItem,
    QProgressDialog,
    QSize,
    Qt,
    QCoreApplication,
    QMessageBox,
    QPoint,
    QApplication,
    QImage,
    QColor,
    QPainter,
    QPointF,
    QInputDialog,
    QFileInfo,
)

from core.io import QTIMAGES
from core.libs import NumberSynthesis, topo
from core.graphics import (
    graph,
    engines,
    EngineError,
)
from .Ui_Permutations import Ui_Form


class NumberAndTypeSynthesis(QWidget, Ui_Form):
    
    """Number and type synthesis widget.
    
    Calculate the combinations of mechanism family and show the atlas.
    """
    
    def __init__(self, parent):
        """Reference names:
        
        + IO functions from main window.
        + Table data from PMKS expression.
        + Graph data function from main window.
        """
        super(NumberAndTypeSynthesis, self).__init__(parent)
        self.setupUi(self)
        self.save_edges_auto_label.setStatusTip(self.save_edges_auto.statusTip())
        
        #Function references
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.inputFrom = parent.inputFrom
        self.jointDataFunc = parent.EntitiesPoint.data
        self.linkDataFunc = parent.EntitiesLink.data
        self.getGraph = parent.getGraph
        
        #Splitters
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 15)
        
        self.answer = []
        
        #Signals
        self.NL_input.valueChanged.connect(self.__adjustStructureData)
        self.NJ_input.valueChanged.connect(self.__adjustStructureData)
        self.graph_engine.addItems(engines)
        self.graph_engine.setCurrentIndex(2)
        self.graph_link_as_node.clicked.connect(self.on_reload_atlas_clicked)
        self.graph_engine.currentIndexChanged.connect(
            self.on_reload_atlas_clicked
        )
        self.Topologic_result.customContextMenuRequested.connect(
            self.__topologicResultContextMenu
        )
        
        """Context menu
        
        + Add to collections
        + Copy edges
        + Copy image
        """
        self.popMenu_topo = QMenu(self)
        self.add_collection = QAction(
            QIcon(QPixmap(":/icons/collections.png")),
            "Add to collections",
            self
        )
        self.copy_edges = QAction("Copy edges", self)
        self.copy_image = QAction("Copy image", self)
        self.popMenu_topo.addActions([
            self.add_collection,
            self.copy_edges,
            self.copy_image
        ])
        self.clear()
    
    def clear(self):
        """Clear all sub-widgets."""
        self.answer.clear()
        self.Expression_edges.clear()
        self.Expression_number.clear()
        self.Topologic_result.clear()
        self.time_label.setText("")
        self.NL_input.setValue(0)
        self.NJ_input.setValue(0)
        self.NL_input_old_value = 0
        self.NJ_input_old_value = 0
        self.DOF.setValue(1)
    
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        """Reload button: Auto-combine the mechanism from the workbook."""
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        if jointData and linkData:
            self.Expression_edges.setText(str(self.getGraph()))
        else:
            self.Expression_edges.setText("")
        keep_dof_checked = self.keep_dof.isChecked()
        self.keep_dof.setChecked(False)
        self.NL_input.setValue(
            sum(len(vlink.points)>1 for vlink in linkData)+
            sum(
                len(vpoint.links)-1 for vpoint in jointData
                if (vpoint.type == 2) and (len(vpoint.links) > 1)
            )
        )
        self.NJ_input.setValue(sum(
            (len(vpoint.links)-1 + int(vpoint.type == 2))
            for vpoint in jointData if len(vpoint.links)>1
        ))
        self.keep_dof.setChecked(keep_dof_checked)
    
    def __adjustStructureData(self):
        """Update NJ and NL values.
        
        If user don't want to keep the DOF:
        Change the DOF then exit.
        """
        if not self.keep_dof.isChecked():
            self.DOF.setValue(
                3 * (self.NL_input.value() - 1) -
                2 * self.NJ_input.value()
            )
            return
        """Prepare the input value.
        
        + N2: Get the user's adjusted value.
        + NL_func: Get the another value of parameters (N1) by
            degrees of freedom formula.
        + is_above: Is value increase or decrease?
        """
        if self.sender() == self.NJ_input:
            N2 = self.NJ_input.value()
            NL_func = lambda: float(((self.DOF.value() + 2*N2) / 3) + 1)
            is_above = N2 > self.NJ_input_old_value
        else:
            N2 = self.NL_input.value()
            NL_func = lambda: float((3*(N2-1) - self.DOF.value()) / 2)
            is_above = N2 > self.NL_input_old_value
        N1 = NL_func()
        while not N1.is_integer():
            N2 += 1 if is_above else -1
            N1 = NL_func()
            if (N1 == 0) or (N2 == 0):
                break
        """Return the result values.
        
        + Value of widgets.
        + Setting old value record.
        """
        if self.sender() == self.NL_input:
            self.NJ_input.setValue(N1)
            self.NL_input.setValue(N2)
            self.NJ_input_old_value = N1
            self.NL_input_old_value = N2
        else:
            self.NJ_input.setValue(N2)
            self.NL_input.setValue(N1)
            self.NJ_input_old_value = N2
            self.NL_input_old_value = N1
    
    @pyqtSlot()
    def on_Combine_number_clicked(self):
        """Show number of links with different number of joints."""
        self.Expression_number.clear()
        NS_result = NumberSynthesis(self.NL_input.value(), self.NJ_input.value())
        if type(NS_result) == str:
            item = QListWidgetItem(NS_result)
            item.links = None
            self.Expression_number.addItem(item)
        else:
            for result in NS_result:
                item = QListWidgetItem(", ".join(
                    "NL{} = {}".format(i+2, result[i])
                    for i in range(len(result))
                ))
                item.links = result
                self.Expression_number.addItem(item)
        self.Expression_number.setCurrentRow(0)
    
    @pyqtSlot()
    def on_Combine_type_clicked(self):
        """Type synthesis.
        
        If there has no data of number synthesis,
        execute number synthesis first.
        """
        row = self.Expression_number.currentRow()
        if not row>-1:
            self.on_Combine_number_clicked()
            row = self.Expression_number.currentRow()
        if self.Expression_number.currentItem() is None:
            return
        answer = self.__typeCombine(row)
        if answer:
            self.answer = answer
            self.on_reload_atlas_clicked()
    
    @pyqtSlot()
    def on_Combine_type_all_clicked(self):
        """Type synthesis - find all.
        
        If the data of number synthesis has multiple results,
        execute type synthesis one by one.
        """
        if not self.Expression_number.currentRow()>-1:
            self.on_Combine_number_clicked()
        if self.Expression_number.currentItem().links is None:
            return
        answers = []
        break_point = False
        for row in range(self.Expression_number.count()):
            answer = self.__typeCombine(row)
            if answer:
                answers += answer
            else:
                break_point = True
                break
        if not answers:
            return
        if break_point:
            reply = QMessageBox.question(self,
                "Type synthesis - abort",
                "Do you want to keep the results?"
            )
            if reply != QMessageBox.Yes:
                return
        self.answer = answers
        self.on_reload_atlas_clicked()
    
    def __typeCombine(self, row: int) -> List[Graph]:
        """Combine and show progress dialog."""
        item = self.Expression_number.item(row)
        progdlg = QProgressDialog(
            "Analysis of the topology...",
            "Cancel",
            0,
            100,
            self
        )
        progdlg.setAttribute(Qt.WA_DeleteOnClose, True)
        progdlg.setWindowTitle("Type synthesis - ({})".format(item.text()))
        progdlg.setMinimumSize(QSize(500, 120))
        progdlg.setModal(True)
        progdlg.show()
        
        def stopFunc():
            """If stop by GUI."""
            QCoreApplication.processEvents()
            progdlg.setValue(progdlg.value() + 1)
            return progdlg.wasCanceled()
        
        def setjobFunc(job: str, maximum: float):
            """New job."""
            progdlg.setLabelText(job)
            progdlg.setValue(0)
            progdlg.setMaximum(maximum+1)
        
        answer, time = topo(
            item.links,
            not self.graph_degenerate.isChecked(),
            setjobFunc,
            stopFunc
        )
        self.time_label.setText("{}[min] {:.2f}[s]".format(
            int(time // 60),
            time % 60
        ))
        progdlg.setValue(progdlg.maximum())
        if answer:
            return [Graph(G.edges) for G in answer]
    
    @pyqtSlot()
    @pyqtSlot(str)
    def on_reload_atlas_clicked(self, p0: Optional[str] = None):
        """Reload the atlas. Regardless there has any old data."""
        self.engine = self.graph_engine.currentText().split(" - ")[1]
        self.Topologic_result.clear()
        if self.answer:
            progdlg = QProgressDialog(
                "Drawing atlas...",
                "Cancel",
                0,
                len(self.answer),
                self
            )
            progdlg.setAttribute(Qt.WA_DeleteOnClose, True)
            progdlg.setWindowTitle("Type synthesis")
            progdlg.resize(400, progdlg.height())
            progdlg.setModal(True)
            progdlg.show()
            for i, G in enumerate(self.answer):
                QCoreApplication.processEvents()
                if progdlg.wasCanceled():
                    return
                if self.__drawAtlas(i, G):
                    progdlg.setValue(i+1)
                else:
                    break
            progdlg.setValue(progdlg.maximum())
    
    def __drawAtlas(self, i: int, G: Graph) -> bool:
        """Draw atlas and return True if done."""
        item = QListWidgetItem("No. {}".format(i + 1))
        try:
            item.setIcon(graph(
                G,
                self.Topologic_result.iconSize().width(),
                self.engine,
                self.graph_link_as_node.isChecked()
            ))
        except EngineError as e:
            QMessageBox.warning(self,
                str(e),
                "Please install and make sure Graphviz is working."
            )
            return False
        else:
            item.setToolTip(str(G.edges))
            self.Topologic_result.addItem(item)
            return True
    
    def __atlasImage(self, row: int =None) -> QImage:
        """Capture a result item icon to image."""
        w = self.Topologic_result
        if row is None:
            item = w.currentItem()
        else:
            item = w.item(row)
        return item.icon().pixmap(w.iconSize()).toImage()
    
    @pyqtSlot(QPoint)
    def __topologicResultContextMenu(self, point):
        """Context menu for the type synthesis results."""
        index = self.Topologic_result.currentIndex().row()
        self.add_collection.setEnabled(index>-1)
        self.copy_edges.setEnabled(index>-1)
        self.copy_image.setEnabled(index>-1)
        action = self.popMenu_topo.exec_(self.Topologic_result.mapToGlobal(point))
        if not action:
            return
        clipboard = QApplication.clipboard()
        if action==self.add_collection:
            self.addCollection(self.answer[index].edges)
        elif action==self.copy_edges:
            clipboard.setText(str(self.answer[index].edges))
        elif action==self.copy_image:
            #Turn the transparent background to white.
            image1 = self.__atlasImage()
            image2 = QImage(image1.size(), image1.format())
            image2.fill(QColor(Qt.white).rgb())
            painter = QPainter(image2)
            painter.drawImage(QPointF(0, 0), image1)
            painter.end()
            pixmap = QPixmap()
            pixmap.convertFromImage(image2)
            clipboard.setPixmap(pixmap)
    
    @pyqtSlot()
    def on_Expression_copy_clicked(self):
        """Copy expression button."""
        string = self.Expression_edges.text()
        if string:
            QApplication.clipboard().setText(string)
            self.Expression_edges.selectAll()
    
    @pyqtSlot()
    def on_Expression_add_collection_clicked(self):
        """Add this expression to collections widget."""
        string = self.Expression_edges.text()
        if string:
            self.addCollection(eval(string))
    
    @pyqtSlot()
    def on_save_atlas_clicked(self):
        """Saving all the atlas to image file.
        
        We should turn transparent background to white first.
        Then using QImage class to merge into one image.
        """
        file_name = ""
        lateral = 0
        if self.save_edges_auto.isChecked():
            lateral, ok = QInputDialog.getInt(self,
                "Atlas",
                "The number of lateral:",
                5, 1, 10
            )
            if not ok:
                return
            file_name = self.outputTo("Atlas image", QTIMAGES)
            if file_name:
                reply = QMessageBox.question(self,
                    "Type synthesis",
                    "Do you want to Re-synthesis?",
                    (QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.Cancel),
                    QMessageBox.YesToAll
                )
                if reply == QMessageBox.Yes:
                    self.on_Combine_type_clicked()
                elif reply == QMessageBox.YesToAll:
                    self.on_Combine_type_all_clicked()
        count = self.Topologic_result.count()
        if not count:
            return
        if not lateral:
            lateral, ok = QInputDialog.getInt(self,
                "Atlas",
                "The number of lateral:",
                5, 1, 10
            )
        if not ok:
            return
        if not file_name:
            file_name = self.outputTo("Atlas image", QTIMAGES)
        if not file_name:
            return
        width = self.Topologic_result.iconSize().width()
        image_main = QImage(
            QSize(
                lateral * width if count>lateral else count * width,
                ((count // lateral) + bool(count % lateral)) * width
            ),
            self.__atlasImage(0).format()
        )
        image_main.fill(QColor(Qt.white).rgb())
        painter = QPainter(image_main)
        for row in range(count):
            image = self.__atlasImage(row)
            painter.drawImage(QPointF(
                row % lateral * width,
                row // lateral * width
            ), image)
        painter.end()
        pixmap = QPixmap()
        pixmap.convertFromImage(image_main)
        pixmap.save(file_name, format=QFileInfo(file_name).suffix())
        self.saveReplyBox("Atlas", file_name)
    
    @pyqtSlot()
    def on_save_edges_clicked(self):
        """Saving all the atlas to text file."""
        file_name = ""
        if self.save_edges_auto.isChecked():
            file_name = self.outputTo(
                "Atlas edges expression",
                ["Text file (*.txt)"]
            )
            if not file_name:
                return
            reply = QMessageBox.question(self,
                "Type synthesis",
                "Do you want to Re-synthesis?",
                (QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.Cancel),
                QMessageBox.YesToAll
            )
            if reply == QMessageBox.Yes:
                self.on_Combine_type_clicked()
            elif reply == QMessageBox.YesToAll:
                self.on_Combine_type_all_clicked()
        count = self.Topologic_result.count()
        if not count:
            return
        if not file_name:
            file_name = self.outputTo(
                "Atlas edges expression",
                ["Text file (*.txt)"]
            )
        if not file_name:
            return
        with open(file_name, 'w') as f:
            f.write('\n'.join(str(G.edges) for G in self.answer))
        self.saveReplyBox("edges expression", file_name)
    
    @pyqtSlot()
    def on_Edges_to_altas_clicked(self):
        """Turn the text files into a atlas image.
        
        This opreation will load all edges to list widget first.
        """
        file_names = self.inputFrom(
            "Edges data",
            ["Text File (*.txt)"],
            multiple=True
        )
        if not file_names:
            return
        read_data = []
        for file_name in file_names:
            with open(file_name, 'r') as f:
                read_data += f.read().split('\n')
        answer = []
        for edges in read_data:
            try:
                answer.append(Graph(eval(edges)))
            except:
                QMessageBox.warning(self,
                    "Wrong format",
                    "Please check the edges text format."
                )
                return
        if not answer:
            return
        self.answer = answer
        self.on_reload_atlas_clicked()
        check_status = self.save_edges_auto.isChecked()
        self.save_edges_auto.setChecked(False)
        self.on_save_atlas_clicked()
        self.save_edges_auto.setChecked(check_status)
