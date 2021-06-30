# -*- coding: utf-8 -*-

"""The widget of 'Structure' tab."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, List, Tuple, Sequence, Dict, Iterable
from qtpy.QtCore import Signal, Slot, Qt, QSize, QPointF, QCoreApplication
from qtpy.QtWidgets import (
    QMessageBox,
    QProgressDialog,
    QListWidgetItem,
    QInputDialog,
    QWidget,
    QApplication,
)
from qtpy.QtGui import QImage, QPainter, QPixmap
from pyslvs.graph import (
    Graph,
    link_assortment,
    contracted_link_assortment,
    labeled_enumerate,
    is_planar,
    external_loop_layout,
)
from pyslvs_ui.qt_patch import qt_image_format
from pyslvs_ui.graphics import graph2icon, engine_picker, engines
from .dialogs.targets import TargetsDialog
from .structure_widget_ui import Ui_Form

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase


class StructureWidget(QWidget, Ui_Form):
    """Structure widget.

    Preview the structures that was been added in collection list by user.
    """
    collections: List[Graph]
    collections_layouts: List[Dict[int, Tuple[float, float]]]
    collections_grounded: List[Graph]

    layout_sender = Signal(Graph, dict)

    def __init__(self, parent: MainWindowBase):
        """Get IO dialog functions from parent."""
        super(StructureWidget, self).__init__(parent)
        self.setupUi(self)
        self.output_to = parent.output_to
        self.save_reply_box = parent.save_reply_box
        self.input_from_multiple = parent.input_from_multiple
        self.add_points_by_graph = parent.add_points_by_graph
        self.project_no_save = parent.project_no_save
        self.prefer = parent.prefer

        # Data structures
        self.collections = []
        self.collections_layouts = []
        self.collections_grounded = []

        # Engine list
        self.graph_engine.addItems(engines)

    def clear(self) -> None:
        """Clear all sub-widgets."""
        for button in (
            self.merge_btn,
            self.configure_btn,
            self.duplicate_btn,
        ):
            button.setEnabled(False)
        self.collections.clear()
        self.collection_list.clear()
        self.__clear_selection()

    @Slot(name='on_clear_btn_clicked')
    def __user_clear(self) -> None:
        """Ask user before clear."""
        if not self.collections:
            return
        if QMessageBox.question(
            self,
            "Delete",
            "Sure to remove all your collections?"
        ) != QMessageBox.Yes:
            return
        self.clear()
        self.project_no_save()

    @Slot(name='on_reload_atlas_clicked')
    @Slot(bool, name='on_graph_link_as_node_toggled')
    @Slot(bool, name='on_graph_show_label_toggled')
    @Slot(int, name='on_graph_engine_currentIndexChanged')
    def __reload_atlas(self) -> None:
        """Reload atlas with the engine."""
        current_pos = self.collection_list.currentRow()
        self.collections_layouts.clear()
        self.collection_list.clear()
        self.__clear_selection()
        if not self.collections:
            return
        dlg = QProgressDialog(
            "Drawing atlas...",
            "Cancel",
            0,
            len(self.collections),
            self
        )
        dlg.setWindowTitle("Type synthesis")
        dlg.resize(400, dlg.height())
        dlg.setModal(True)
        dlg.show()
        engine_str = self.graph_engine.currentText()
        for i, g in enumerate(self.collections):
            QCoreApplication.processEvents()
            if dlg.wasCanceled():
                dlg.deleteLater()
                return
            item = QListWidgetItem(f"No. {i + 1}")
            pos = engine_picker(g, engine_str, self.graph_link_as_node.isChecked())
            item.setIcon(graph2icon(
                g,
                self.collection_list.iconSize().width(),
                self.graph_link_as_node.isChecked(),
                self.graph_show_label.isChecked(),
                self.prefer.monochrome_option,
                pos=pos
            ))
            self.collections_layouts.append(dict(pos))
            item.setToolTip(f"{g.edges}")
            self.collection_list.addItem(item)
            dlg.setValue(i + 1)
        dlg.deleteLater()
        if current_pos > -1:
            self.collection_list.setCurrentRow(current_pos)
            self.__set_selection(self.collection_list.currentItem())

    def __is_valid_graph(self, edges: Iterable[Tuple[int, int]]) -> str:
        """Test graph and return True if it is valid."""
        try:
            g = Graph(edges)
        except (TypeError, ValueError):
            return "wrong format"
        if not g.edges:
            return "is an empty graph"
        if not g.is_connected():
            return "is not a close chain"
        if not is_planar(g):
            return "is not a planar chain"
        if g.has_cut_link():
            return "has cut link"
        try:
            external_loop_layout(g, True)
        except ValueError as error:
            return str(error)
        for h in self.collections:
            if g.is_isomorphic(h):
                return f"is isomorphic with: {h.edges}"
        return ""

    def add_collection(self, edges: Iterable[Tuple[int, int]], *, reload: bool = True) -> None:
        """Add collection by in put edges."""
        error = self.__is_valid_graph(edges)
        if error:
            QMessageBox.warning(self, "Add Collection Error", f"Error: {error}")
            return
        self.collections.append(Graph(edges))
        self.project_no_save()
        if reload:
            self.__reload_atlas()

    def add_collections(self, collections: Sequence[Sequence[Tuple[int, int]]]) -> None:
        """Add collections."""
        for edges in collections:
            self.add_collection(edges)

    @Slot(name='on_add_by_edges_btn_clicked')
    def __add_from_edges(self) -> None:
        """Add collection by input string."""
        edges_str = ""
        while not edges_str:
            edges_str, ok = QInputDialog.getText(
                self,
                "Add by edges",
                "Please enter a connection expression:\n"
                "Example: [(0, 1), (1, 2), (2, 3), (3, 0)]"
            )
            if not ok:
                return
        try:
            edges = eval(edges_str)
            if any(len(edge) != 2 for edge in edges):
                raise ValueError("wrong format")
        except (SyntaxError, ValueError) as error:
            QMessageBox.warning(self, str(error), f"Error: {error}")
            return
        else:
            self.add_collection(edges)

    @Slot(name='on_add_by_files_btn_clicked')
    def __add_from_files(self) -> None:
        """Append atlas by text files."""
        file_names = self.input_from_multiple(
            "edges data",
            ["Text File (*.txt)"]
        )
        if not file_names:
            return
        read_data = []
        for file_name in file_names:
            with open(file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    read_data.append(line)
        errors = []
        for edges_str in read_data:
            try:
                edges = eval(edges_str)
                if any(len(edge) != 2 for edge in edges):
                    raise ValueError("wrong format")
            except (SyntaxError, ValueError) as error:
                errors.append(str(error))
            else:
                self.add_collection(edges, reload=False)
        if errors:
            QMessageBox.warning(self, "Loaded Error", "Error:" + '\n'.join(errors))
        self.__reload_atlas()

    @Slot(name='on_capture_graph_clicked')
    def __save_graph(self) -> None:
        """Save the current graph."""
        if self.selection_window.count() != 1:
            return
        file_name = self.output_to("atlas image", qt_image_format)
        if not file_name:
            return
        pixmap: QPixmap = self.selection_window.item(0).icon().pixmap(self.selection_window.iconSize())
        pixmap.save(file_name)
        self.save_reply_box("Graph", file_name)

    @Slot(name='on_save_atlas_clicked')
    def __save_atlas(self) -> None:
        """Save function as same as type synthesis widget."""
        count = self.collection_list.count()
        if count < 1:
            return
        lateral, ok = QInputDialog.getInt(
            self,
            "Atlas",
            "The number of lateral:",
            5, 1
        )
        if not ok:
            return
        file_name = self.output_to("atlas image", qt_image_format)
        if not file_name:
            return
        icon_size = self.collection_list.iconSize()
        width = icon_size.width()
        image = self.collection_list.item(0).icon().pixmap(icon_size).toImage()
        image_main = QImage(QSize(
            lateral if count > lateral else count,
            (count // lateral) + bool(count % lateral)
        ) * width, image.format())
        image_main.fill(Qt.transparent)
        painter = QPainter(image_main)
        for row in range(count):
            image = self.collection_list.item(row).icon().pixmap(icon_size).toImage()
            painter.drawImage(QPointF(row % lateral, row // lateral) * width, image)
        painter.end()
        pixmap = QPixmap()
        pixmap.convertFromImage(image_main)
        pixmap.save(file_name)
        self.save_reply_box("Atlas", file_name)

    @Slot(name='on_save_edges_clicked')
    def __save_edges(self) -> None:
        """Save function as same as type synthesis widget."""
        count = self.collection_list.count()
        if count < 1:
            return
        file_name = self.output_to("atlas edges expression", ["Text file (*.txt)"])
        if not file_name:
            return
        with open(file_name, 'w+', encoding='utf-8') as f:
            f.write('\n'.join(str(g.edges) for g in self.collections))
        self.save_reply_box("edges expression", file_name)

    @Slot(QListWidgetItem, name='on_collection_list_itemClicked')
    def __set_selection(self, item: QListWidgetItem) -> None:
        """Show the data of collection.

        Save the layout position to keep the graphs
        will be in same appearance.
        """
        for button in (
            self.delete_btn,
            self.configure_btn,
            self.duplicate_btn,
        ):
            button.setEnabled(item is not None)
        self.selection_window.clear()
        if item is None:
            return
        # Preview item
        link_is_node = self.graph_link_as_node.isChecked()
        item_preview = QListWidgetItem(item.text())
        row = self.collection_list.row(item)
        g = self.collections[row]
        self.ground_engine = self.collections_layouts[row]
        item_preview.setIcon(graph2icon(
            g,
            self.selection_window.iconSize().width(),
            link_is_node,
            self.graph_show_label.isChecked(),
            self.prefer.monochrome_option,
            pos=self.ground_engine
        ))
        self.selection_window.addItem(item_preview)
        # Set attributes
        self.edges_text.setText(str(list(g.edges)))
        self.nl_label.setText(str(len(g.vertices)))
        self.nj_label.setText(str(len(g.edges)))
        self.dof_label.setText(str(g.dof()))
        self.is_degenerate_label.setText(str(g.is_degenerate()))
        self.link_assortment_label.setText(str(link_assortment(g)))
        self.contracted_link_assortment_label.setText(str(contracted_link_assortment(g)))
        # Buttons
        self.duplicate_btn.setEnabled(link_is_node)
        self.configure_btn.setEnabled(not link_is_node)
        self.merge_btn.setEnabled(not link_is_node)
        self.__grounded()

    def __clear_selection(self) -> None:
        """Clear the selection preview data."""
        self.grounded_list.clear()
        self.selection_window.clear()
        self.edges_text.clear()
        self.nl_label.setText('0')
        self.nj_label.setText('0')
        self.dof_label.setText('0')
        self.is_degenerate_label.setText("N/A")
        self.link_assortment_label.setText("N/A")
        self.contracted_link_assortment_label.setText("N/A")

    @Slot(name='on_expr_copy_clicked')
    def __copy_expr(self) -> None:
        """Copy the expression."""
        string = self.edges_text.text()
        if string:
            QApplication.clipboard().setText(string)
            self.edges_text.selectAll()

    @Slot(name='on_delete_btn_clicked')
    def __delete_collection(self) -> None:
        """Delete the selected collection."""
        row = self.collection_list.currentRow()
        if not row > -1:
            return
        if QMessageBox.question(
            self,
            "Delete",
            f"Sure to remove #{row} from your collections?"
        ) != QMessageBox.Yes:
            return
        self.collection_list.takeItem(row)
        self.collections.pop(row)
        self.collections_layouts.pop(row)
        self.__clear_selection()
        self.project_no_save()

    @Slot(name='on_duplicate_btn_clicked')
    def __make_duplicate(self) -> None:
        """Make current graph symmetric."""
        row = self.collection_list.currentRow()
        if not row > -1:
            return
        graph = self.collections[row]
        dlg = TargetsDialog(
            "Select the vertices (links) you want to copy.\n"
            "The duplication will keep adjacency",
            "",
            graph.vertices,
            (),
            self
        )
        dlg.show()
        if not dlg.exec_():
            dlg.deleteLater()
            return
        targets = dlg.targets()
        dlg.deleteLater()
        times, ok = QInputDialog.getInt(
            self,
            "Make duplicate",
            "The count of duplication:",
            1, 1
        )
        if not ok:
            return
        new_graph = graph.duplicate(targets, times)
        self.add_collection(new_graph.edges)

    @Slot(name='on_configure_btn_clicked')
    def __configuration(self) -> None:
        """Triangular iteration."""
        self.layout_sender.emit(
            self.collections[self.collection_list.currentRow()],
            self.ground_engine.copy()
        )

    def __grounded(self) -> None:
        """Grounded combinations."""
        current_item = self.collection_list.currentItem()
        self.collections_grounded.clear()
        self.grounded_list.clear()
        g = self.collections[self.collection_list.row(current_item)]
        item = QListWidgetItem("Released")
        icon = graph2icon(
            g,
            self.grounded_list.iconSize().width(),
            self.graph_link_as_node.isChecked(),
            self.graph_show_label.isChecked(),
            self.prefer.monochrome_option,
            pos=self.ground_engine
        )
        item.setIcon(icon)
        self.collections_grounded.append(g)
        self.grounded_list.addItem(item)
        for node, graph_ in labeled_enumerate(g):
            item = QListWidgetItem(f"link_{node}")
            icon = graph2icon(
                g,
                self.grounded_list.iconSize().width(),
                self.graph_link_as_node.isChecked(),
                self.graph_show_label.isChecked(),
                self.prefer.monochrome_option,
                except_node=node,
                pos=self.ground_engine
            )
            item.setIcon(icon)
            self.collections_grounded.append(graph_)
            self.grounded_list.addItem(item)

    @Slot(name='on_merge_btn_clicked')
    def __grounded_merge(self) -> None:
        """Merge the grounded result."""
        item = self.grounded_list.currentItem()
        if not item:
            return
        graph = self.collections_grounded[0]
        text = item.text()
        if text == "Released":
            ground_link = None
        else:
            ground_link = int(text.split("_")[1])
        if QMessageBox.question(
            self,
            "Message",
            f"Merge \"{text}\" chain to your canvas?"
        ) == QMessageBox.Yes:
            self.add_points_by_graph(
                graph,
                self.ground_engine,
                ground_link
            )
