# -*- coding: utf-8 -*-

"""'structure_synthesis' module contains
number and type _synthesis functional interfaces.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Sequence,
    Iterator,
    Iterable,
    Optional,
)
from time import time
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
    QPainter,
    QPointF,
    QInputDialog,
    QFileInfo,
    QScrollBar,
)
from core import main_window as mw
from core.libs import (
    number_synthesis,
    contracted_link,
    topo,
    VPoint,
    Graph,
    link_assortments as l_a,
    contracted_link_assortments as c_l_a,
)
from core.graphics import (
    to_graph,
    engines,
)
from .Ui_structure_widget import Ui_Form

__all__ = ['StructureSynthesis']


def _link_assortments(links_expr: str) -> List[int]:
    """Return link assortment from expr."""
    return [int(n.split('=')[-1]) for n in links_expr.split(", ")]


def compare_assortment(first: Tuple[int, ...], second: Sequence[Tuple[int, ...]]) -> int:
    """Compare assortment."""
    my_len = len(first)
    for i, job in enumerate(second):
        if job == first + (0,) * (len(job) - my_len):
            return i
    return -1


class SynthesisProgressDialog(QProgressDialog):

    """Progress dialog for structure _synthesis."""

    def __init__(self, title: str, job_name: str, maximum: int, parent: QWidget):
        super(SynthesisProgressDialog, self).__init__(
            job_name,
            "Interrupt",
            0,
            maximum,
            parent
        )
        self.setWindowTitle(title)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(400, self.height())
        self.setModal(True)
        self.setValue(0)

    def next(self):
        """Increase value of progress bar."""
        self.setValue(self.value() + 1)

    def stop_func(self) -> bool:
        """Return dialog status."""
        try:
            QCoreApplication.processEvents()
            return self.wasCanceled()
        except RuntimeError:
            return False


class StructureSynthesis(QWidget, Ui_Form):
    """Number and type _synthesis widget.

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

        # Answer list.
        self.answer: List[Graph] = []

        # Signals
        self.NL_input.valueChanged.connect(self.__adjust_structure_data)
        self.NJ_input.valueChanged.connect(self.__adjust_structure_data)
        self.graph_engine.addItems(engines)
        self.structure_list.customContextMenuRequested.connect(
            self.__structure_list_context_menu
        )

        """Context menu

        + Add to collections
        + Copy edges
        + Copy image
        """
        self.pop_menu_topo = QMenu(self)
        self.add_collection = QAction(
            QIcon(QPixmap(":/icons/collections.png")),
            "Add to collections",
            self
        )
        self.copy_edges = QAction("Copy edges", self)
        self.copy_image = QAction("Copy image", self)
        self.pop_menu_topo.addActions([
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
        self.l_a_list.clear()
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
            graph = Graph(self.getGraph())
            self.edges_text.setText(str(graph.edges))
        else:
            graph = Graph([])
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

        # Auto _synthesis.
        if not graph.edges:
            return

        l_a_row = compare_assortment(tuple(l_a(graph)), self.__l_a_synthesis())
        self.l_a_list.setCurrentRow(l_a_row)
        self.c_l_a_list.setCurrentRow(compare_assortment(tuple(c_l_a(graph)), self.__c_l_a_synthesis(l_a_row)))

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

        # Prepare the input value.
        # + N2: Get the user's adjusted value.
        # + NL_func: Get the another value of parameters (N1) by degrees of freedom formula.
        # + is_above: Is value increase or decrease?
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

        # Return the result values.
        # + Value of widgets.
        # + Setting old value record.
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
    def __l_a_synthesis(self) -> List[Tuple[int, ...]]:
        """Synthesis of link assortments."""
        self.l_a_list.clear()
        self.c_l_a_list.clear()

        nl = self.NL_input.value()
        nj = self.NJ_input.value()
        dlg = SynthesisProgressDialog(
            "Link assortments",
            f"({nl}, {nj})",
            1,
            self
        )
        dlg.show()
        try:
            results = number_synthesis(nl, nj, dlg.stop_func)
        except Exception as e:
            item = QListWidgetItem(str(e))
            self.l_a_list.addItem(item)
            dlg.next()
            return []
        else:
            for result in results:
                self.l_a_list.addItem(QListWidgetItem(", ".join(
                    f"NL{i + 2} = {result[i]}" for i in range(len(result))
                )))
            self.l_a_list.setCurrentRow(0)
            dlg.next()
            return results

    @pyqtSlot(int, name='on_l_a_list_currentRowChanged')
    def __c_l_a_synthesis(self, l_a_row: int = 0) -> List[Tuple[int, ...]]:
        """Synthesis of contracted link assortments."""
        self.c_l_a_list.clear()
        item = self.l_a_list.item(l_a_row)
        if item is None:
            return []

        job_l_a = _link_assortments(item.text())
        dlg = SynthesisProgressDialog(
            "Contracted link assortments",
            str(job_l_a),
            1,
            self
        )
        dlg.show()
        results = contracted_link(job_l_a, dlg.stop_func)
        for c_j in results:
            self.c_l_a_list.addItem(QListWidgetItem(", ".join(
                f"Nc{i + 1} = {c_j[i]}" for i in range(len(c_j))
            )))
        self.c_l_a_list.setCurrentRow(0)
        dlg.next()
        return results

    def __set_time_count(self, t: float, count: int):
        """Set time and count digit to label."""
        self.time_label.setText(f"{t:.04f} s ({count})")

    def __set_paint_time(self, t: float):
        """Set painting time of atlas."""
        self.paint_time_label.setText(f"{t:.04f}s")

    @pyqtSlot(name='on_structure_synthesis_button_clicked')
    def __structure_synthesis(self):
        """Structural _synthesis - find by contracted links."""
        self.__clear_structure_list()
        row = self.l_a_list.currentRow()
        if row == -1:
            self.__l_a_synthesis()
            self.__c_l_a_synthesis()
        item_l_a: QListWidgetItem = self.l_a_list.currentItem()
        item_c_l_a: QListWidgetItem = self.c_l_a_list.currentItem()
        try:
            job_l_a = _link_assortments(item_l_a.text())
            job_c_l_a = _link_assortments(item_c_l_a.text())
        except ValueError:
            return

        self.__structural_combine([(job_l_a, job_c_l_a)], 1)

    @pyqtSlot(name='on_structure_synthesis_links_button_clicked')
    def __structure_synthesis_links(self):
        """Structural _synthesis - find by links."""
        self.__clear_structure_list()
        row = self.l_a_list.currentRow()
        if row == -1:
            self.__l_a_synthesis()
            self.__c_l_a_synthesis()
        item_l_a: QListWidgetItem = self.l_a_list.currentItem()
        try:
            job_l_a = _link_assortments(item_l_a.text())
        except ValueError:
            return

        jobs = contracted_link(job_l_a)

        def jobs_iterator(
            _l_a: Sequence[int],
            _jobs: Sequence[Sequence[int]]
        ) -> Iterator[Tuple[Sequence[int], Sequence[int]]]:
            for _c_l_a in _jobs:
                yield _l_a, _c_l_a

        self.__structural_combine(jobs_iterator(job_l_a, jobs), len(jobs))

    @pyqtSlot(name='on_structure_synthesis_all_button_clicked')
    def __structure_synthesis_all(self):
        """Structural _synthesis - find all."""
        self.__clear_structure_list()
        if self.l_a_list.currentRow() == -1:
            self.__l_a_synthesis()
        item: QListWidgetItem = self.c_l_a_list.currentItem()
        try:
            _link_assortments(item.text())
        except ValueError:
            return

        job_count = 0
        jobs = []
        for row in range(self.l_a_list.count()):
            item: QListWidgetItem = self.l_a_list.item(row)
            job_l_a = _link_assortments(item.text())
            job_c_l_as = contracted_link(job_l_a)
            job_count += len(job_c_l_as)
            jobs.append((job_l_a, job_c_l_as))

        def jobs_iterator(
            _jobs: Sequence[Tuple[Sequence[int], Sequence[Sequence[int]]]]
        ) -> Iterator[Tuple[Sequence[int], Sequence[int]]]:
            for _l_a, _c_l_as in _jobs:
                for _c_l_a in _c_l_as:
                    yield _l_a, _c_l_a

        self.__structural_combine(jobs_iterator(jobs), job_count)

    def __structural_combine(
        self,
        jobs: Iterable[Tuple[Sequence[int], Sequence[int]]],
        job_count: int
    ):
        """Structural combine by iterator."""
        dlg = SynthesisProgressDialog("Structural Synthesis", "", job_count, self)
        dlg.show()

        answers = []
        break_point = False
        t0 = 0.
        c0 = 0
        for job_l_a, job_c_l_a in jobs:
            answer, t1 = topo(
                job_l_a,
                job_c_l_a,
                self.graph_degenerate.currentIndex(),
                dlg.stop_func
            )
            dlg.next()
            if answer is not None:
                answers.extend(answer)
                t0 += t1
                c0 += len(answer)
            else:
                break_point = True
                break

        if not answers:
            return

        if break_point:
            reply = QMessageBox.question(
                self,
                "Type _synthesis - abort",
                "Do you want to keep the results?"
            )
            if reply != QMessageBox.Yes:
                return

        # Save the answer list.
        self.answer = answers
        self.__set_time_count(t0, c0)
        self.__reload_atlas()

    @pyqtSlot(name='on_graph_link_as_node_clicked')
    @pyqtSlot(name='on_graph_show_label_clicked')
    @pyqtSlot(name='on_reload_atlas_clicked')
    @pyqtSlot(int, name='on_graph_engine_currentIndexChanged')
    def __reload_atlas(self, *_: int):
        """Reload the atlas."""
        scroll_bar: QScrollBar = self.structure_list.verticalScrollBar()
        scroll_pos = scroll_bar.sliderPosition()
        self.structure_list.clear()

        if not self.answer:
            return

        dlg = SynthesisProgressDialog(
            "Type _synthesis",
            "Drawing atlas...",
            len(self.answer),
            self
        )
        dlg.show()
        t0 = time()
        for i, G in enumerate(self.answer):
            QCoreApplication.processEvents()
            if dlg.wasCanceled():
                return
            if self.__draw_atlas(i, G):
                dlg.setValue(i + 1)
            else:
                break
        self.__set_paint_time(time() - t0)
        dlg.setValue(dlg.maximum())
        scroll_bar.setSliderPosition(scroll_pos)

    def __draw_atlas(self, i: int, g: Graph) -> bool:
        """Draw atlas and return True if done."""
        item = QListWidgetItem(f"No. {i + 1}")
        item.setIcon(to_graph(
            g,
            self.structure_list.iconSize().width(),
            self.graph_engine.currentText(),
            self.graph_link_as_node.isChecked(),
            self.graph_show_label.isChecked()
        ))
        item.setToolTip(
            f"Edge Set: {list(g.edges)}\n"
            f"Link Assortments: {l_a(g)}\n"
            f"Contracted Link Assortments: {c_l_a(g)}"
        )
        self.structure_list.addItem(item)
        return True

    def __atlas_image(self, row: Optional[int] = None) -> QImage:
        """Capture a result item icon to image."""
        if row is None:
            item: QListWidgetItem = self.structure_list.currentItem()
        else:
            item: QListWidgetItem = self.structure_list.item(row)
        icon: QIcon = item.icon()
        pixmap: QPixmap = icon.pixmap(self.structure_list.iconSize())
        return pixmap.toImage()

    @pyqtSlot(QPoint)
    def __structure_list_context_menu(self, point):
        """Context menu for the type _synthesis results."""
        index = self.structure_list.currentIndex().row()
        self.add_collection.setEnabled(index > -1)
        self.copy_edges.setEnabled(index > -1)
        self.copy_image.setEnabled(index > -1)
        action = self.pop_menu_topo.exec_(self.structure_list.mapToGlobal(point))
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
            image2.fill(Qt.white)
            painter = QPainter(image2)
            painter.drawImage(QPointF(0, 0), image1)
            painter.end()
            clipboard.setPixmap(QPixmap.fromImage(image2))

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
        count = self.structure_list.count()
        if not count:
            return

        lateral = self.__save_atlas_ask()
        if not lateral:
            return

        file_name = self.outputTo("Atlas image", qt_image_format)
        if not file_name:
            return

        width = self.structure_list.iconSize().width()
        image_main = QImage(QSize(
            lateral * width if count > lateral else count * width,
            ((count // lateral) + bool(count % lateral)) * width
        ), self.__atlas_image(0).format())
        image_main.fill(Qt.transparent)
        painter = QPainter(image_main)
        for row in range(count):
            image = self.__atlas_image(row)
            painter.drawImage(QPointF(
                row % lateral * width,
                row // lateral * width
            ), image)
        painter.end()
        pixmap = QPixmap.fromImage(image_main)
        pixmap.save(file_name, format=QFileInfo(file_name).suffix())
        self.saveReplyBox("Atlas", file_name)

    def __save_atlas_ask(self) -> int:
        """Ask when saving the atlas."""
        lateral, ok = QInputDialog.getInt(
            self,
            "Atlas",
            "The number of lateral:",
            5,
            1
        )
        if not ok:
            return 0
        return lateral

    @pyqtSlot(name='on_save_edges_clicked')
    def __save_edges(self):
        """Saving all the atlas to text file."""
        file_name = ""
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
                    read_data.append(line)

        answer = []
        for edges in read_data:
            try:
                g = Graph(eval(edges))
            except (SyntaxError, TypeError):
                QMessageBox.warning(
                    self,
                    "Wrong format",
                    "Please check text format."
                )
            else:
                answer.append(g)

        if not answer:
            QMessageBox.information(
                self,
                "No data",
                "The graph data is empty."
            )
            return

        self.answer = answer
        self.__reload_atlas()
        self.__save_atlas()
