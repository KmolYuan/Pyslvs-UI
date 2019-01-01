# -*- coding: utf-8 -*-

"""The widget of 'Structure' tab."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    List,
    Tuple,
    Sequence,
    Dict,
    Optional,
)
from core.QtModules import (
    pyqtSignal,
    pyqtSlot,
    qt_image_format,
    Qt,
    QMessageBox,
    QProgressDialog,
    QCoreApplication,
    QListWidgetItem,
    QInputDialog,
    QImage,
    QSize,
    QWidget,
    QPainter,
    QPointF,
    QPixmap,
    QFileInfo,
    QApplication,
)
from core import main_window as mw
from core.graphics import (
    to_graph,
    engine_picker,
    engines,
)
from core.libs import (
    Graph,
    link_assortments as l_a,
    contracted_link_assortments as c_l_a,
    is_planar,
)
from .Ui_structure_widget import Ui_Form


class _TestError(Exception):
    """Error raise while add a graphs."""
    pass


class StructureWidget(QWidget, Ui_Form):

    """Structure widget.

    Preview the structures that was been added in collection list by user.
    """

    layout_sender = pyqtSignal(Graph, dict)

    def __init__(self, parent: 'mw.MainWindow'):
        """Get IO dialog functions from parent."""
        super(StructureWidget, self).__init__(parent)
        self.setupUi(self)
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.inputFrom = parent.inputFrom
        self.addPointsByGraph = parent.addPointsByGraph
        self.unsaveFunc = parent.workbookNoSave

        # Data structures.
        self.collections: List[Graph] = []
        self.collections_layouts: List[Dict[int, Tuple[float, float]]] = []
        self.collections_grounded: List[Graph] = []

        # Engine list.
        self.graph_engine.addItems(engines)

    def clear(self):
        """Clear all sub-widgets."""
        self.grounded_merge.setEnabled(False)
        self.triangle_button.setEnabled(False)
        self.collections.clear()
        self.collection_list.clear()
        self.__clear_selection()

    @pyqtSlot(name='on_clear_button_clicked')
    def __user_clear(self):
        """Ask user before clear."""
        if not self.collections:
            return
        reply = QMessageBox.question(
            self,
            "Delete",
            "Sure to remove all your collections?"
        )
        if reply != QMessageBox.Yes:
            return
        self.clear()
        self.unsaveFunc()

    @pyqtSlot(name='on_graph_link_as_node_clicked')
    @pyqtSlot(name='on_graph_show_label_clicked')
    @pyqtSlot(name='on_reload_atlas_clicked')
    @pyqtSlot(int, name='on_graph_engine_currentIndexChanged')
    def __reload_atlas(self):
        """Reload atlas with the engine."""
        current_pos = self.collection_list.currentRow()
        self.collections_layouts.clear()
        self.collection_list.clear()
        self.__clear_selection()

        if not self.collections:
            return

        progress_dlg = QProgressDialog(
            "Drawing atlas...",
            "Cancel",
            0,
            len(self.collections),
            self
        )
        progress_dlg.setAttribute(Qt.WA_DeleteOnClose, True)
        progress_dlg.setWindowTitle("Type synthesis")
        progress_dlg.resize(400, progress_dlg.height())
        progress_dlg.setModal(True)
        progress_dlg.show()
        engine_str = self.graph_engine.currentText()
        for i, g in enumerate(self.collections):
            QCoreApplication.processEvents()
            if progress_dlg.wasCanceled():
                return
            item = QListWidgetItem(f"No. {i + 1}")
            engine = engine_picker(g, engine_str, self.graph_link_as_node.isChecked())
            item.setIcon(to_graph(
                g,
                self.collection_list.iconSize().width(),
                engine,
                self.graph_link_as_node.isChecked(),
                self.graph_show_label.isChecked()
            ))
            self.collections_layouts.append(engine)
            item.setToolTip(f"{g.edges}")
            self.collection_list.addItem(item)
            progress_dlg.setValue(i + 1)

        self.collection_list.setCurrentRow(current_pos)

    def addCollection(self, edges: Sequence[Tuple[int, int]]):
        """Add collection by in put edges."""
        graph = Graph(edges)
        try:
            if not edges:
                raise _TestError("is an empty graph")
            if not graph.is_connected():
                raise _TestError("is not a close chain")
            if not is_planar(graph):
                raise _TestError("is not a planar chain")
            for graph_ in self.collections:
                if graph.is_isomorphic(graph_):
                    raise _TestError(f"is isomorphic with: {graph_.edges}")
        except _TestError as e:
            QMessageBox.warning(self, "Add Collection Error", f"Error: {e}")
            return
        self.collections.append(graph)
        self.unsaveFunc()
        self.__reload_atlas()

    def addCollections(self, collections: Sequence[Sequence[Tuple[int, int]]]):
        """Add collections."""
        for c in collections:
            self.addCollection(c)

    @pyqtSlot(name='on_add_by_edges_button_clicked')
    def __add_from_edges(self):
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
                raise IOError("wrong format")
        except Exception as e:
            QMessageBox.warning(self, str(e), f"Error: {e}")
            return
        else:
            self.addCollection(edges)

    @pyqtSlot(name='on_add_by_files_button_clicked')
    def __add_from_files(self):
        """Append atlas by text files."""
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
                for line in f:
                    read_data.append(line[:-1])
        collections = []
        for edges in read_data:
            try:
                collections.append(Graph(eval(edges)))
            except (SyntaxError, TypeError):
                QMessageBox.warning(
                    self,
                    "Wrong format",
                    "Please check the edges text format."
                )
                return
        if not collections:
            return
        self.collections += collections
        self.__reload_atlas()

    @pyqtSlot(name='on_save_atlas_clicked')
    def __save_atlas(self):
        """Save function as same as type synthesis widget."""
        count = self.collection_list.count()
        if not count:
            return

        lateral, ok = QInputDialog.getInt(
            self,
            "Atlas",
            "The number of lateral:",
            5,
            1
        )
        if not ok:
            return

        file_name = self.outputTo("Atlas image", qt_image_format)
        if not file_name:
            return

        icon_size = self.collection_list.iconSize()
        width = icon_size.width()
        image_main = QImage(QSize(
            lateral * width if count > lateral else count * width,
            ((count // lateral) + bool(count % lateral)) * width
        ), self.collection_list.item(0).icon().pixmap(icon_size).toImage().format())
        image_main.fill(Qt.transparent)
        painter = QPainter(image_main)
        for row in range(count):
            image = self.collection_list.item(row).icon().pixmap(icon_size).toImage()
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
        """Save function as same as type synthesis widget."""
        count = self.collection_list.count()
        if not count:
            return
        file_name = self.outputTo("Atlas edges expression", ["Text file (*.txt)"])
        if not file_name:
            return
        with open(file_name, 'w') as f:
            f.write('\n'.join(str(G.edges) for G in self.collections))
        self.saveReplyBox("edges expression", file_name)

    @pyqtSlot(int, name='on_collection_list_currentRowChanged')
    def __set_selection(self, row: int):
        """Show the data of collection.

        Save the layout position to keep the graphs
        will be in same appearance.
        """
        item: Optional[QListWidgetItem] = self.collection_list.item(row)
        has_item = item is not None
        self.delete_button.setEnabled(has_item)
        self.grounded_button.setEnabled(has_item)
        self.triangle_button.setEnabled(has_item)
        self.selection_window.clear()
        if item is None:
            return

        # Preview item.
        link_is_node = self.graph_link_as_node.isChecked()
        item_preview = QListWidgetItem(item.text())
        row = self.collection_list.row(item)
        g = self.collections[row]
        self.ground_engine = self.collections_layouts[row]
        item_preview.setIcon(to_graph(
            g,
            self.selection_window.iconSize().width(),
            self.ground_engine,
            link_is_node,
            self.graph_show_label.isChecked()
        ))
        self.selection_window.addItem(item_preview)

        # Set attributes.
        self.edges_text.setText(str(list(g.edges)))
        self.nl_label.setText(str(len(g.nodes)))
        self.nj_label.setText(str(len(g.edges)))
        self.dof_label.setText(str(g.dof()))
        self.is_degenerate_label.setText(str(g.is_degenerate()))
        self.link_assortments_label.setText(str(l_a(g)))
        self.contracted_link_assortments_label.setText(str(c_l_a(g)))

        # "Link as node" layout cannot do these action.
        self.triangle_button.setEnabled(not link_is_node)
        self.grounded_merge.setEnabled(not link_is_node)

    def __clear_selection(self):
        """Clear the selection preview data."""
        self.grounded_list.clear()
        self.selection_window.clear()
        self.edges_text.clear()
        self.nl_label.setText('0')
        self.nj_label.setText('0')
        self.dof_label.setText('0')
        self.is_degenerate_label.setText("N/A")
        self.link_assortments_label.setText("N/A")
        self.contracted_link_assortments_label.setText("N/A")

    @pyqtSlot(name='on_expr_copy_clicked')
    def __copy_expr(self):
        """Copy the expression."""
        string = self.edges_text.text()
        if string:
            QApplication.clipboard().setText(string)
            self.edges_text.selectAll()

    @pyqtSlot(name='on_delete_button_clicked')
    def __delete_collection(self):
        """Delete the selected collection."""
        row = self.collection_list.currentRow()
        if not row > -1:
            return
        reply = QMessageBox.question(
            self,
            "Delete",
            f"Sure to remove # {row} from your collections?"
        )
        if reply != QMessageBox.Yes:
            return
        self.__clear_selection()
        self.collection_list.takeItem(row)
        del self.collections[row]
        self.unsaveFunc()

    @pyqtSlot(name='on_triangle_button_clicked')
    def __triangulation(self):
        """Triangular iteration."""
        self.layout_sender.emit(
            self.collections[self.collection_list.currentRow()],
            self.ground_engine
        )

    @pyqtSlot(name='on_grounded_button_clicked')
    def __grounded(self):
        """Grounded combinations."""
        current_item = self.collection_list.currentItem()
        self.collections_grounded.clear()
        self.grounded_list.clear()
        g = self.collections[self.collection_list.row(current_item)]
        item = QListWidgetItem("Released")
        icon = to_graph(
            g,
            self.grounded_list.iconSize().width(),
            self.ground_engine,
            self.graph_link_as_node.isChecked(),
            self.graph_show_label.isChecked()
        )
        item.setIcon(icon)
        self.collections_grounded.append(g)
        self.grounded_list.addItem(item)

        def isomorphic(g: Graph, l: List[Graph]) -> bool:
            for h in l:
                if g.is_isomorphic(h):
                    return True
            return False

        for node in g.nodes:
            graph_ = Graph([e for e in g.edges if node not in e])
            if isomorphic(graph_, self.collections_grounded):
                continue
            item = QListWidgetItem(f"link_{node}")
            icon = to_graph(
                g,
                self.grounded_list.iconSize().width(),
                self.ground_engine,
                self.graph_link_as_node.isChecked(),
                self.graph_show_label.isChecked(),
                except_node=node
            )
            item.setIcon(icon)
            self.collections_grounded.append(graph_)
            self.grounded_list.addItem(item)

    @pyqtSlot(name='on_grounded_merge_clicked')
    def __grounded_merge(self):
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
        reply = QMessageBox.question(
            self,
            "Message",
            f"Merge \"{text}\" chain to your canvas?"
        )
        if reply == QMessageBox.Yes:
            self.addPointsByGraph(
                graph,
                self.ground_engine,
                ground_link
            )
