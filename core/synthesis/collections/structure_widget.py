# -*- coding: utf-8 -*-

"""The widget of 'Structure' tab."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
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
    QColor,
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
        for i, graph in enumerate(self.collections):
            QCoreApplication.processEvents()
            if progress_dlg.wasCanceled():
                return
            item = QListWidgetItem(f"No. {i + 1}")
            engine = engine_picker(graph, engine_str, self.graph_link_as_node.isChecked())
            item.setIcon(to_graph(
                graph,
                self.collection_list.iconSize().width(),
                engine,
                self.graph_link_as_node.isChecked()
            ))
            self.collections_layouts.append(engine)
            item.setToolTip(f"{graph.edges}\nUse the right-click menu to operate.")
            self.collection_list.addItem(item)
            progress_dlg.setValue(i + 1)

        self.collection_list.setCurrentRow(current_pos)

    def addCollection(self, edges: Sequence[Tuple[int, int]]):
        """Add collection by in put edges."""
        graph = Graph(edges)
        try:
            if not edges:
                raise _TestError("is empty graph.")
            for n in graph.nodes:
                if len(list(graph.neighbors(n))) < 2:
                    raise _TestError("is not close chain")
            for H in self.collections:
                if graph.is_isomorphic(H):
                    raise _TestError("is isomorphic")
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
                raise IOError("Wrong format")
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
            5, 1, 10
        )
        if not ok:
            return
        file_name = self.outputTo("Atlas image", qt_image_format)
        if not file_name:
            return
        icon_size = self.collection_list.iconSize()
        width = icon_size.width()
        image_main = QImage(
            QSize(
                lateral * width if count > lateral else count * width,
                ((count // lateral) + bool(count % lateral)) * width
            ),
            self.collection_list.item(0).icon().pixmap(icon_size).toImage().format()
        )
        image_main.fill(QColor(Qt.white).rgb())
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
        if item is None:
            return

        self.selection_window.clear()
        item_ = QListWidgetItem(item.text())
        row = self.collection_list.row(item)
        graph = self.collections[row]
        self.ground_engine = self.collections_layouts[row]
        item_.setIcon(to_graph(
            graph,
            self.selection_window.iconSize().width(),
            self.ground_engine,
            self.graph_link_as_node.isChecked()
        ))
        self.selection_window.addItem(item_)
        self.edges_text.setText(str(list(graph.edges)))
        self.nl_label.setText(str(len(graph.nodes)))
        self.nj_label.setText(str(len(graph.edges)))
        self.dof_label.setText(str(graph.dof()))
        self.link_assortments_label.setText(str(l_a(graph)))
        self.contracted_link_assortments_label.setText(str(c_l_a(graph)))

    def __clear_selection(self):
        """Clear the selection preview data."""
        self.grounded_list.clear()
        self.selection_window.clear()
        self.edges_text.clear()
        self.nl_label.setText('0')
        self.nj_label.setText('0')
        self.dof_label.setText('0')
        self.link_assortments_label.setText("")
        self.contracted_link_assortments_label.setText("")

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
        graph = self.collections[self.collection_list.row(current_item)]
        item = QListWidgetItem("Released")
        icon = to_graph(
            graph,
            self.grounded_list.iconSize().width(),
            self.ground_engine,
            self.graph_link_as_node.isChecked()
        )
        item.setIcon(icon)
        self.collections_grounded.append(graph)
        self.grounded_list.addItem(item)

        def isomorphic(g: Graph, l: List[Graph]) -> bool:
            for h in l:
                if g.is_isomorphic(h):
                    return True
            return False

        for node in graph.nodes:
            graph_ = Graph([e for e in graph.edges if node not in e])
            if isomorphic(graph_, self.collections_grounded):
                continue
            item = QListWidgetItem(f"link_{node}")
            icon = to_graph(
                graph,
                self.grounded_list.iconSize().width(),
                self.ground_engine,
                self.graph_link_as_node.isChecked(),
                except_node=node
            )
            item.setIcon(icon)
            self.collections_grounded.append(graph_)
            self.grounded_list.addItem(item)

        # "Link as node" layout cannot be merged.
        self.grounded_merge.setEnabled(not self.graph_link_as_node.isChecked())

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
