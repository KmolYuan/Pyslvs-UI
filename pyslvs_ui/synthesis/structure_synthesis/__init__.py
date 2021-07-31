# -*- coding: utf-8 -*-

"""'structure_synthesis' module contains
number and type synthesis functional interfaces.
"""

from __future__ import annotations

__all__ = ['StructureSynthesis']
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, List, Sequence, Dict, Optional
from time import process_time
from qtpy.QtCore import (
    Slot,
    Qt,
    QSize,
    QCoreApplication,
    QPoint,
    QPointF,
)
from qtpy.QtWidgets import (
    QWidget,
    QMenu,
    QAction,
    QProgressDialog,
    QMessageBox,
    QApplication,
    QInputDialog,
    QScrollBar,
    QListWidgetItem,
    QTreeWidgetItem,
    QHeaderView,
)
from qtpy.QtGui import QIcon, QPixmap, QImage, QPainter
from pyslvs.graph import Graph, link_assortment, contracted_link_assortment
from pyslvs_ui.qt_patch import qt_image_format
from pyslvs_ui.graphics import graph2icon, engines
from .thread import assortment_eval, LinkThread, GraphThread
from .structure_widget_ui import Ui_Form

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase

Assortment = Sequence[int]


class SynthesisProgressDialog(QProgressDialog):
    """Progress dialog for structure synthesis."""

    def __init__(self, title: str, job_name: str, maximum: int, parent: QWidget):
        super(SynthesisProgressDialog, self).__init__(
            job_name,
            "Interrupt",
            0,
            maximum,
            parent
        )
        self.setWindowTitle(title)
        self.resize(400, self.height())
        self.setModal(True)
        self.setValue(0)

    def stop_func(self) -> bool:
        """Return dialog status."""
        try:
            QCoreApplication.processEvents()
            return self.wasCanceled()
        except ValueError:
            return False


class StructureSynthesis(QWidget, Ui_Form):
    """Number and type synthesis widget.

    Calculate the combinations of mechanism family and show the atlas.
    """
    assortment: Dict[Assortment, List[Assortment]]
    answer: List[Graph]

    def __init__(self, parent: MainWindowBase):
        """Reference names:

        + IO functions from main window.
        + Table data from PMKS expression.
        + Graph data function from main window.
        """
        super(StructureSynthesis, self).__init__(parent)
        self.setupUi(self)
        header = self.link_assortment_list.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Function references
        self.output_to = parent.output_to
        self.save_reply_box = parent.save_reply_box
        self.input_from_multiple = parent.input_from_multiple
        self.vpoints = parent.vpoint_list
        self.vlinks = parent.vlink_list
        self.get_graph = parent.get_graph
        self.prefer = parent.prefer
        self.add_collection = parent.collections.structure_widget.add_collection
        # Answer list
        self.assortment = {}
        self.answer = []
        # Signals
        self.nl_input.valueChanged.connect(self.__adjust_structure_data)
        self.nj_input.valueChanged.connect(self.__adjust_structure_data)
        self.graph_engine.addItems(engines)
        self.structure_list.customContextMenuRequested.connect(
            self.__structure_list_context_menu
        )

        # Context menu
        self.pop_menu_topo = QMenu(self)
        self.to_collection = QAction(
            QIcon(QPixmap("icons:collections.png")),
            "Add to collections",
            self
        )
        self.copy_edges = QAction("Copy edges", self)
        self.copy_image = QAction("Copy image", self)
        self.pop_menu_topo.addActions([
            self.to_collection,
            self.copy_edges,
            self.copy_image,
        ])

        self.nl_input_old_value = 0
        self.nj_input_old_value = 0
        self.clear()

    def clear(self) -> None:
        """Clear all sub-widgets."""
        self.edges_text.clear()
        self.__clear_assortment()
        self.__clear_structure_list()
        self.nl_input.setValue(0)
        self.nj_input.setValue(0)
        self.nl_input_old_value = 0
        self.nj_input_old_value = 0
        self.dof.setValue(1)

    @Slot(name='on_assortment_clear_btn_clicked')
    def __clear_assortment(self) -> None:
        """Clear the number synthesis list."""
        self.link_assortment_list.clear()
        self.assortment.clear()

    @Slot(name='on_structure_list_clear_btn_clicked')
    def __clear_structure_list(self) -> None:
        """Clear the structure list."""
        self.answer.clear()
        self.structure_list.clear()
        self.time_label.setText("")

    @Slot(name='on_from_mechanism_btn_clicked')
    def __from_mechanism(self) -> None:
        """From a generalized mechanism of main canvas."""
        if self.vpoints and self.vlinks:
            graph, _, _, _, _, _ = self.get_graph()
        else:
            graph = Graph([])
        if graph.edges:
            self.edges_text.setText(str(list(graph.edges)))
        else:
            self.edges_text.setText("")
        keep_dof_checked = self.keep_dof.isChecked()
        self.keep_dof.setChecked(False)
        self.nl_input.setValue(len(graph.vertices))
        self.nj_input.setValue(len(graph.edges))
        self.keep_dof.setChecked(keep_dof_checked)

        # Show attributes
        QMessageBox.information(
            self,
            "Generalization",
            f"Link assortment:\n{link_assortment(graph)}\n"
            f"Contracted link assortment:\n{contracted_link_assortment(graph)}"
            if graph.edges else
            "Is a empty graph."
        )

    def __adjust_structure_data(self) -> None:
        """Update NJ and NL values.

        If user don't want to keep the DOF:
        Change the DOF then exit.
        """
        if not self.keep_dof.isChecked():
            self.dof.setValue(
                3 * (self.nl_input.value() - 1)
                - 2 * self.nj_input.value()
            )
            return

        # N2: Get the user's adjusted value.
        # NL_func: Get the another value of parameters (N1) by degrees of freedom formula.
        # is_above: Is value increase or decrease?
        if self.sender() is self.nj_input:
            n2 = self.nj_input.value()

            def nl_func() -> float:
                return (self.dof.value() + 2 * n2) / 3 + 1

            is_above = n2 > self.nj_input_old_value
        else:
            n2 = self.nl_input.value()

            def nl_func() -> float:
                return (3 * (n2 - 1) - self.dof.value()) / 2

            is_above = n2 > self.nl_input_old_value
        n1 = nl_func()
        while not n1.is_integer():
            n2 += 1 if is_above else -1
            n1 = nl_func()
            if n1 == 0 or n2 == 0:
                break

        n1 = int(n1)
        n2 = int(n2)
        # Return the result values
        # + Value of widgets.
        # + Setting old value record.
        if self.sender() is self.nl_input:
            self.nj_input.setValue(n1)
            self.nl_input.setValue(n2)
            self.nj_input_old_value = n1
            self.nl_input_old_value = n2
        else:
            self.nj_input.setValue(n2)
            self.nl_input.setValue(n1)
            self.nj_input_old_value = n2
            self.nl_input_old_value = n1

    @Slot(name='on_number_synthesis_btn_clicked')
    def __number_synthesis(self) -> None:
        """Synthesis of link assortment."""
        self.__clear_assortment()
        nl = self.nl_input.value()
        nj = self.nj_input.value()
        dlg = SynthesisProgressDialog(
            "Link assortment",
            f"Number of links: {nl}\n"
            f"Number of joints: {nj}",
            1,
            self
        )

        @Slot(dict)
        def update_result(assortment: Dict[Assortment, List[Assortment]]) -> None:
            """Update results."""
            self.assortment.update(assortment)
            for la, cla_list in assortment.items():
                la_item = QTreeWidgetItem([", ".join(
                    f"NL{i + 2} = {a}" for i, a in enumerate(la)
                ), "N/A"])
                for cla in cla_list:
                    la_item.addChild(QTreeWidgetItem([", ".join(
                        f"NC{i + 1} = {a}" for i, a in enumerate(cla)
                    ), "N/A"]))
                self.link_assortment_list.addTopLevelItem(la_item)
            first_item = self.link_assortment_list.topLevelItem(0)
            self.link_assortment_list.setCurrentItem(first_item)
            dlg.deleteLater()

        work = LinkThread(nl, nj, dlg)
        work.progress_update.connect(dlg.setValue)
        work.size_update.connect(dlg.setMaximum)
        work.result.connect(update_result)
        dlg.show()
        work.start()

    def __set_time_count(self, t: float, count: int) -> None:
        """Set time and count digit to label."""
        self.time_label.setText(f"{t:.04f} s ({count})")

    def __set_paint_time(self, t: float) -> None:
        """Set painting time of atlas."""
        self.paint_time_label.setText(f"{t:.04f}s")

    @Slot(name='on_structure_synthesis_btn_clicked')
    def __structure_synthesis(self) -> None:
        """Structural synthesis - find by contracted links."""
        self.__clear_structure_list()
        item = self.link_assortment_list.currentItem()
        if item is None:
            self.__number_synthesis()
            item = self.link_assortment_list.currentItem()
        root = item.parent()
        if root is None:
            # Find by link assortment
            try:
                # Test
                assortment_eval(item.text(0))
            except ValueError:
                return
            jobs = [item.child(i) for i in range(item.childCount())]
        else:
            # Find by contracted link assortment
            jobs = [item]
        self.__structural_combine(jobs)

    @Slot(name='on_structure_synthesis_all_btn_clicked')
    def __structure_synthesis_all(self) -> None:
        """Structural synthesis - find all."""
        self.__clear_structure_list()
        jobs = []
        for i in range(self.link_assortment_list.topLevelItemCount()):
            root = self.link_assortment_list.topLevelItem(i)
            for j in range(root.childCount()):
                jobs.append(root.child(j))
        self.__structural_combine(jobs)

    def __structural_combine(self, jobs: Sequence[QTreeWidgetItem]) -> None:
        """Structural combine by iterator."""
        t0 = process_time()
        dlg = SynthesisProgressDialog(
            "Structural Synthesis",
            f"Number of cases: {len(jobs)}",
            len(jobs),
            self
        )

        @Slot(QTreeWidgetItem, int)
        def update_count(item: QTreeWidgetItem, count: int) -> None:
            """Update the number of graphs."""
            item.setText(1, f"{count}")

        @Slot(list)
        def update_result(answer: List[Graph]) -> None:
            """Update the result of atlas."""
            self.answer = answer
            dlg.deleteLater()
            for i in range(self.link_assortment_list.topLevelItemCount()):
                root = self.link_assortment_list.topLevelItem(i)
                count = 0
                for j in range(root.childCount()):
                    item = root.child(j)
                    try:
                        count += int(item.text(1))
                    except ValueError:
                        pass
                root.setText(1, f"{count}")
            self.__set_time_count(process_time() - t0, len(self.answer))
            self.__reload_atlas()

        work = GraphThread(jobs, self.graph_degenerate.currentIndex(), dlg)
        work.count_update.connect(update_count)
        work.progress_update.connect(dlg.setValue)
        work.result.connect(update_result)
        dlg.show()
        work.start()

    @Slot(name='on_reload_atlas_clicked')
    @Slot(bool, name='on_graph_link_as_node_toggled')
    @Slot(bool, name='on_graph_show_label_toggled')
    @Slot(int, name='on_graph_engine_currentIndexChanged')
    def __reload_atlas(self, *_) -> None:
        """Reload the atlas."""
        scroll_bar: QScrollBar = self.structure_list.verticalScrollBar()
        scroll_pos = scroll_bar.sliderPosition()
        index = self.structure_list.currentRow()
        self.structure_list.clear()

        if not self.answer:
            return

        dlg = SynthesisProgressDialog(
            "Structural Synthesis",
            f"Drawing atlas ({len(self.answer)}) ...",
            len(self.answer),
            self
        )
        dlg.show()
        t0 = process_time()
        for i, G in enumerate(self.answer):
            QCoreApplication.processEvents()
            if dlg.wasCanceled():
                return
            if self.__draw_atlas(i, G):
                dlg.setValue(i + 1)
            else:
                break
        self.__set_paint_time(process_time() - t0)
        dlg.setValue(dlg.maximum())
        dlg.deleteLater()
        scroll_bar.setSliderPosition(scroll_pos)
        self.structure_list.setCurrentRow(index)

    def __draw_atlas(self, i: int, g: Graph) -> bool:
        """Draw atlas and return True if done."""
        item = QListWidgetItem(f"No. {i + 1}")
        item.setIcon(graph2icon(
            g,
            self.structure_list.iconSize().width(),
            self.graph_link_as_node.isChecked(),
            self.graph_show_label.isChecked(),
            self.prefer.monochrome_option,
            engine=self.graph_engine.currentText()
        ))
        item.setToolTip(
            f"Edge Set: {list(g.edges)}\n"
            f"Link assortment: {link_assortment(g)}\n"
            f"Contracted Link assortment: {contracted_link_assortment(g)}\n"
            f"Degree code: {g.degree_code()}"
        )
        self.structure_list.addItem(item)
        return True

    def __atlas_image(self, row: Optional[int] = None) -> QImage:
        """Capture a result item icon to image."""
        if row is None:
            item = self.structure_list.currentItem()
        else:
            item = self.structure_list.item(row)
        return item.icon().pixmap(self.structure_list.iconSize()).toImage()

    @Slot(QPoint)
    def __structure_list_context_menu(self, point) -> None:
        """Context menu for the type synthesis results."""
        index = self.structure_list.currentIndex().row()
        self.to_collection.setEnabled(index > -1)
        self.copy_edges.setEnabled(index > -1)
        self.copy_image.setEnabled(index > -1)
        action = self.pop_menu_topo.exec_(self.structure_list.mapToGlobal(point))
        if not action:
            return
        clipboard = QApplication.clipboard()
        if action == self.to_collection:
            self.add_collection(self.answer[index].edges)
        elif action == self.copy_edges:
            clipboard.setText(str(self.answer[index].edges))
        elif action == self.copy_image:
            # Turn the transparent background to white
            image1 = self.__atlas_image()
            image2 = QImage(image1.size(), image1.format())
            image2.fill(Qt.white)
            painter = QPainter(image2)
            painter.drawImage(QPointF(0, 0), image1)
            painter.end()
            clipboard.setPixmap(QPixmap.fromImage(image2))

    @Slot(name='on_expr_copy_clicked')
    def __copy_expr(self) -> None:
        """Copy expression button."""
        string = self.edges_text.text()
        if string:
            QApplication.clipboard().setText(string)
            self.edges_text.selectAll()

    @Slot(name='on_expr_add_collection_clicked')
    def __add_collection(self) -> None:
        """Add this expression to collections widget."""
        string = self.edges_text.text()
        if string:
            self.add_collection(eval(string))

    @Slot(name='on_save_atlas_clicked')
    def __save_atlas(self) -> None:
        """Saving all the atlas to image file.

        We should turn transparent background to white first.
        Then using QImage class to merge into one image.
        """
        count = self.structure_list.count()
        if count < 1:
            return

        lateral = self.__save_atlas_ask()
        if not lateral:
            return

        file_name = self.output_to("atlas image", qt_image_format)
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
            painter.drawImage(QPointF(row % lateral, row // lateral) * width, image)
        painter.end()
        pixmap = QPixmap.fromImage(image_main)
        pixmap.save(file_name)
        self.save_reply_box("Atlas", file_name)

    def __save_atlas_ask(self) -> int:
        """Ask when saving the atlas."""
        lateral, ok = QInputDialog.getInt(
            self,
            "Atlas",
            "The number of lateral:",
            5, 1
        )
        if not ok:
            return 0
        return lateral

    @Slot(name='on_save_edges_clicked')
    def __save_edges(self) -> None:
        """Saving all the atlas to text file."""
        file_name = ""
        count = self.structure_list.count()
        if count < 1:
            return
        if not file_name:
            file_name = self.output_to("atlas edges expression", ["Text file (*.txt)"])
        if not file_name:
            return
        with open(file_name, 'w+', encoding='utf-8') as f:
            f.write('\n'.join(str(G.edges) for G in self.answer))
        self.save_reply_box("edges expression", file_name)

    @Slot(name='on_edges2atlas_btn_clicked')
    def __edges2atlas(self) -> None:
        """Turn the text files into a atlas image.

        This operation will load all edges to list widget first.
        """
        file_names = self.input_from_multiple(
            "edges data",
            ["Text file (*.txt)"]
        )
        if not file_names:
            return

        read_data = []
        for file_name in file_names:
            with open(file_name, 'r', encoding='utf-8') as f:
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
        self.__set_time_count(0, len(answer))
        self.__reload_atlas()
        self.__save_atlas()
