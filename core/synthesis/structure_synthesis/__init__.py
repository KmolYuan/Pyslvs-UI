# -*- coding: utf-8 -*-

"""'structure_synthesis' module contains
number and type synthesis functional interfaces.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, List, Optional
from networkx import Graph
from networkx.exception import NetworkXError
from core.QtModules import (
    pyqtSlot,
    qt_image_format,
    Qt,
    QWidget,
    QMenu,
    QAction,
    QIcon,
    QPixmap,
    QListWidgetItem,
    QProgressDialog,
    QSize,
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
from core import main_window as mw
from core.libs import number_synthesis, topo, VPoint
from core.graphics import (
    to_graph,
    engines,
    EngineError,
)
from .Ui_structure_widget import Ui_Form

__all__ = ['StructureSynthesis']


def _link_assortment(links_expr: str) -> List[int]:
    """Return link assortment from expr."""
    return [int(n.split('=')[-1]) for n in links_expr.split(", ")]


class SynthesisProgressDialog(QProgressDialog):

    """Progress dialog for structure synthesis."""

    def __init__(self, job_name: str, maximum: int, parent: QWidget):
        super(SynthesisProgressDialog, self).__init__(
            job_name,
            "Interrupt",
            0,
            maximum,
            parent
        )
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(400, self.height())
        self.setModal(True)


class StructureSynthesis(QWidget, Ui_Form):
    """Number and type synthesis widget.

    Calculate the combinations of mechanism family and show the atlas.
    """

    def __init__(self, parent: 'mw.MainWindow'):
        """Reference names:

        + IO functions from main window.
        + Table data from PMKS expression.
        + Graph data function from main window.
        """
        super(StructureSynthesis, self).__init__(parent)
        self.setupUi(self)
        self.save_edges_auto_label.setStatusTip(self.save_edges_auto.statusTip())

        # Function references
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.inputFrom = parent.inputFrom
        self.jointDataFunc = parent.EntitiesPoint.dataTuple
        self.linkDataFunc = parent.EntitiesLink.dataTuple
        self.getGraph = parent.getGraph

        # Splitters
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 15)

        self.answer = []

        # Signals
        self.NL_input.valueChanged.connect(self.__adjust_structure_data)
        self.NJ_input.valueChanged.connect(self.__adjust_structure_data)
        self.graph_engine.addItems(engines)
        self.graph_engine.setCurrentIndex(2)
        self.structure_list.customContextMenuRequested.connect(
            self.__topologic_result_context_menu
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

        self.NL_input_old_value = 0
        self.NJ_input_old_value = 0
        self.clear()

    def clear(self):
        """Clear all sub-widgets."""
        self.answer.clear()
        self.edges_text.clear()
        self.link_assortments_list.clear()
        self.__clear_structure_list()
        self.NL_input.setValue(0)
        self.NJ_input.setValue(0)
        self.NL_input_old_value = 0
        self.NJ_input_old_value = 0
        self.DOF.setValue(1)

    @pyqtSlot(name='on_structure_list_clear_button_clicked')
    def __clear_structure_list(self):
        """Clear the structure list."""
        self.structure_list.clear()
        self.time_label.setText("")

    @pyqtSlot(name='on_from_mechanism_button_clicked')
    def __from_mechanism(self):
        """Reload button: Auto-combine the mechanism from the workbook."""
        joint_data = self.jointDataFunc()
        link_data = self.linkDataFunc()
        if joint_data and link_data:
            self.edges_text.setText(str(self.getGraph()))
        else:
            self.edges_text.setText("")
        keep_dof_checked = self.keep_dof.isChecked()
        self.keep_dof.setChecked(False)
        self.NL_input.setValue(
            sum(len(vlink.points) > 1 for vlink in link_data) +
            sum(
                len(vpoint.links) - 2 for vpoint in joint_data
                if (vpoint.type == VPoint.RP) and (len(vpoint.links) > 1)
            )
        )
        self.NJ_input.setValue(sum(
            (len(vpoint.links) - 1 + int(vpoint.type == VPoint.RP))
            for vpoint in joint_data if (len(vpoint.links) > 1)
        ))
        self.keep_dof.setChecked(keep_dof_checked)

    def __adjust_structure_data(self):
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
            n2 = self.NJ_input.value()

            def nl_func() -> float:
                return ((self.DOF.value() + 2 * n2) / 3) + 1

            is_above = n2 > self.NJ_input_old_value
        else:
            n2 = self.NL_input.value()

            def nl_func() -> float:
                return (3 * (n2 - 1) - self.DOF.value()) / 2

            is_above = n2 > self.NL_input_old_value
        n1 = nl_func()
        while not n1.is_integer():
            n2 += 1 if is_above else -1
            n1 = nl_func()
            if (n1 == 0) or (n2 == 0):
                break
        """Return the result values.

        + Value of widgets.
        + Setting old value record.
        """
        if self.sender() == self.NL_input:
            self.NJ_input.setValue(n1)
            self.NL_input.setValue(n2)
            self.NJ_input_old_value = n1
            self.NL_input_old_value = n2
        else:
            self.NJ_input.setValue(n2)
            self.NL_input.setValue(n1)
            self.NJ_input_old_value = n2
            self.NL_input_old_value = n1

    @pyqtSlot(name='on_number_synthesis_button_clicked')
    def __number_synthesis(self):
        """Show number of links with different number of joints."""
        self.link_assortments_list.clear()
        try:
            results = number_synthesis(self.NL_input.value(), self.NJ_input.value())
        except Exception as e:
            item = QListWidgetItem(str(e))
            self.link_assortments_list.addItem(item)
        else:
            for result in results:
                item = QListWidgetItem(", ".join(
                    f"NL{i + 2} = {result[i]}" for i in range(len(result))
                ))
                self.link_assortments_list.addItem(item)
        self.link_assortments_list.setCurrentRow(0)

    @pyqtSlot(name='on_structure_synthesis_button_clicked')
    def __structure_synthesis(self):
        """Type synthesis.

        If there has no data of number synthesis,
        execute number synthesis first.
        """
        row = self.link_assortments_list.currentRow()
        if not row > -1:
            self.__number_synthesis()
            row = self.link_assortments_list.currentRow()
        if self.link_assortments_list.currentItem() is None:
            return
        answer, t = self.__structural_combine(row)
        self.time_label.setText(f"{t:.04f} s")
        if answer is not None:
            self.answer = answer
            self.__reload_atlas()

    @pyqtSlot(name='on_structure_synthesis_all_button_clicked')
    def __structure_synthesis_all(self):
        """Structure synthesis - find all.

        If the data of number synthesis has multiple results,
        execute type synthesis one by one.
        """
        if not self.link_assortments_list.currentRow() > -1:
            self.__number_synthesis()
        item: QListWidgetItem = self.link_assortments_list.currentItem()
        try:
            _link_assortment(item.text())
        except ValueError:
            return
        answers = []
        break_point = False
        t0 = 0.
        for row in range(self.link_assortments_list.count()):
            answer, t1 = self.__structural_combine(row)
            if answer is not None:
                answers += answer
                t0 += t1
            else:
                break_point = True
                break
        if not answers:
            return
        if break_point:
            reply = QMessageBox.question(
                self,
                "Type synthesis - abort",
                "Do you want to keep the results?"
            )
            if reply != QMessageBox.Yes:
                return
        self.answer = answers
        self.time_label.setText(f"{t0:.04f} s")
        self.__reload_atlas()

    def __structural_combine(self, row: int) -> Tuple[Optional[List[Graph]], float]:
        """Combine and show progress dialog."""
        self.__clear_structure_list()
        item: QListWidgetItem = self.link_assortments_list.item(row)
        item_text = item.text()
        dlg = SynthesisProgressDialog("", 0, self)
        dlg.setWindowTitle(item_text)

        def job_func(cla: List[int], job_count: int):
            """job_func"""
            if cla:
                dlg.setLabelText(dlg.labelText() + str(cla) + '\n')
            dlg.setMaximum(dlg.maximum() + job_count)

        def step_func():
            """step_func"""
            dlg.setValue(dlg.value() + 1)
            QCoreApplication.processEvents()

        def stop_func() -> bool:
            """Return dialog status."""
            try:
                QCoreApplication.processEvents()
                return dlg.wasCanceled()
            except RuntimeError:
                return False

        dlg.show()
        result, time = topo(
            _link_assortment(item_text),
            self.graph_degenerate.currentIndex(),
            job_func,
            step_func,
            stop_func,
        )
        dlg.close()
        return [Graph(g.edges) for g in result], time

    @pyqtSlot(name='on_graph_link_as_node_clicked')
    @pyqtSlot(name='on_reload_atlas_clicked')
    @pyqtSlot(int, name='on_graph_engine_currentIndexChanged')
    def __reload_atlas(self, *_: int):
        """Reload the atlas. Regardless there has any old data."""
        self.engine = self.graph_engine.currentText().split(" - ")[1]
        self.structure_list.clear()
        if self.answer:
            dlg = SynthesisProgressDialog("Drawing atlas...", len(self.answer), self)
            dlg.setWindowTitle("Type synthesis")
            dlg.show()
            for i, G in enumerate(self.answer):
                QCoreApplication.processEvents()
                if dlg.wasCanceled():
                    return
                if self.__draw_atlas(i, G):
                    dlg.setValue(i + 1)
                else:
                    break
            dlg.setValue(dlg.maximum())

    def __draw_atlas(self, i: int, graph: Graph) -> bool:
        """Draw atlas and return True if done."""
        item = QListWidgetItem(f"No. {i + 1}")
        try:
            item.setIcon(to_graph(
                graph,
                self.structure_list.iconSize().width(),
                self.engine,
                self.graph_link_as_node.isChecked()
            ))
        except EngineError as error:
            QMessageBox.warning(
                self,
                f"{error}",
                "Please install and make sure Graphviz is working."
            )
            return False
        else:
            item.setToolTip(str(graph.edges))
            self.structure_list.addItem(item)
            return True

    def __atlas_image(self, row: int = None) -> QImage:
        """Capture a result item icon to image."""
        w = self.structure_list
        if row is None:
            item = w.currentItem()
        else:
            item = w.item(row)
        return item.icon().pixmap(w.iconSize()).toImage()

    @pyqtSlot(QPoint)
    def __topologic_result_context_menu(self, point):
        """Context menu for the type synthesis results."""
        index = self.structure_list.currentIndex().row()
        self.add_collection.setEnabled(index > -1)
        self.copy_edges.setEnabled(index > -1)
        self.copy_image.setEnabled(index > -1)
        action = self.popMenu_topo.exec_(self.structure_list.mapToGlobal(point))
        if not action:
            return
        clipboard = QApplication.clipboard()
        if action == self.add_collection:
            self.addCollection(self.answer[index].edges)
        elif action == self.copy_edges:
            clipboard.setText(str(self.answer[index].edges))
        elif action == self.copy_image:
            # Turn the transparent background to white.
            image1 = self.__atlas_image()
            image2 = QImage(image1.size(), image1.format())
            image2.fill(QColor(Qt.white).rgb())
            painter = QPainter(image2)
            painter.drawImage(QPointF(0, 0), image1)
            painter.end()
            pixmap = QPixmap()
            pixmap.convertFromImage(image2)
            clipboard.setPixmap(pixmap)

    @pyqtSlot(name='on_expr_copy_clicked')
    def __copy_expr(self):
        """Copy expression button."""
        string = self.edges_text.text()
        if string:
            QApplication.clipboard().setText(string)
            self.edges_text.selectAll()

    @pyqtSlot(name='on_expr_add_collection_clicked')
    def __add_collection(self):
        """Add this expression to collections widget."""
        string = self.edges_text.text()
        if string:
            self.addCollection(eval(string))

    @pyqtSlot(name='on_save_atlas_clicked')
    def __save_atlas(self):
        """Saving all the atlas to image file.

        We should turn transparent background to white first.
        Then using QImage class to merge into one image.
        """
        file_name = ""
        lateral = 0
        if self.save_edges_auto.isChecked():
            lateral, ok = QInputDialog.getInt(
                self,
                "Atlas",
                "The number of lateral:",
                5, 1, 10
            )
            if not ok:
                return
            file_name = self.outputTo("Atlas image", qt_image_format)
            if file_name:
                reply = QMessageBox.question(
                    self,
                    "Type synthesis",
                    "Do you want to Re-synthesis?",
                    (QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.Cancel),
                    QMessageBox.Yes
                )
                if reply == QMessageBox.Yes:
                    self.__structure_synthesis()
                elif reply == QMessageBox.YesToAll:
                    self.__structure_synthesis_all()
        count = self.structure_list.count()
        if not count:
            return
        if not lateral:
            lateral, ok = QInputDialog.getInt(
                self,
                "Atlas",
                "The number of lateral:",
                5, 1, 10
            )
            if not ok:
                return
        if not file_name:
            file_name = self.outputTo("Atlas image", qt_image_format)
        if not file_name:
            return
        width = self.structure_list.iconSize().width()
        image_main = QImage(
            QSize(
                lateral * width if count > lateral else count * width,
                ((count // lateral) + bool(count % lateral)) * width
            ),
            self.__atlas_image(0).format()
        )
        image_main.fill(QColor(Qt.white).rgb())
        painter = QPainter(image_main)
        for row in range(count):
            image = self.__atlas_image(row)
            painter.drawImage(QPointF(
                row % lateral * width,
                row // lateral * width
            ), image)
        painter.end()
        pixmap = QPixmap()
        pixmap.convertFromImage(image_main)
        pixmap.save(file_name, format=QFileInfo(file_name).suffix())
        self.saveReplyBox("Atlas", file_name)

    @pyqtSlot(name='on_save_edges_clicked')
    def __save_edges(self):
        """Saving all the atlas to text file."""
        file_name = ""
        if self.save_edges_auto.isChecked():
            file_name = self.outputTo(
                "Atlas edges expression",
                ["Text file (*.txt)"]
            )
            if not file_name:
                return
            reply = QMessageBox.question(
                self,
                "Type synthesis",
                "Do you want to Re-synthesis?",
                (QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.Cancel),
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.__structure_synthesis()
            elif reply == QMessageBox.YesToAll:
                self.__structure_synthesis_all()
        count = self.structure_list.count()
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

    @pyqtSlot(name='on_edges2atlas_button_clicked')
    def __edges2atlas(self):
        """Turn the text files into a atlas image.

        This operation will load all edges to list widget first.
        """
        file_names = self.inputFrom(
            "Edges data",
            ["Text file (*.txt)"],
            multiple=True
        )
        if not file_names:
            return
        read_data = []
        for file_name in file_names:
            with open(file_name) as f:
                for line in f:
                    read_data.append(line[:-1])
        answer = []
        for edges in read_data:
            try:
                answer.append(Graph(eval(edges)))
            except NetworkXError:
                QMessageBox.warning(
                    self,
                    "Wrong format",
                    "Please check the edges text format."
                )
                return
        if not answer:
            return
        self.answer = answer
        self.__reload_atlas()
        self.save_edges_auto.setChecked(False)
        self.__save_atlas()
        self.save_edges_auto.setChecked(self.save_edges_auto.isChecked())
