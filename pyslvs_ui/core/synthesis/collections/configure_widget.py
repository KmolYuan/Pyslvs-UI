# -*- coding: utf-8 -*-

"""The widget of 'Triangular iteration' tab."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    TYPE_CHECKING,
    List,
    Tuple,
    Sequence,
    Dict,
    Callable,
    Optional,
    Any,
)
from math import hypot
import pprint
from pyslvs import (
    Graph,
    edges_view,
    graph2vpoints,
    parse_pos,
)
from pyslvs_ui.core.QtModules import (
    Signal,
    QWidget,
    Slot,
    QMessageBox,
    QInputDialog,
    QListWidgetItem,
    QLabel,
    QApplication,
    QMouseEvent,
)
from pyslvs_ui.core.graphics import PreviewCanvas
from .dialogs import (
    CollectionsDialog,
    CustomsDialog,
    TargetsDialog,
    list_texts,
)
from .configure_widget_ui import Ui_Form
if TYPE_CHECKING:
    from pyslvs_ui.core.widgets.main_base import MainWindowBase

_Coord = Tuple[float, float]


class _ConfigureCanvas(PreviewCanvas):

    """Customized preview window has some functions of mouse interaction.

    Emit signal call to change current point when pressed a dot.
    """

    edit_size = 1000
    set_joint_number = Signal(int)

    def __init__(self, parent: QWidget) -> None:
        """Add a function use to get current point from parent."""
        super(_ConfigureCanvas, self).__init__(parent)
        self.pressed = False
        self.get_joint_number = parent.joint_name.currentIndex

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Check if get close to a joint."""
        mx = (event.x() - self.ox) / self.zoom
        my = (event.y() - self.oy) / -self.zoom

        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue

            if hypot(x - mx, y - my) <= 5:
                self.set_joint_number.emit(node)
                self.pressed = True
                break

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Cancel the drag."""
        self.pressed = False

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Drag to move the joint."""
        if not self.pressed:
            return

        row = self.get_joint_number()
        if not row > -1:
            return

        mx = (event.x() - self.ox) / self.zoom
        my = (event.y() - self.oy) / -self.zoom
        hv = _ConfigureCanvas.edit_size / 2

        if -hv <= mx <= hv:
            self.pos[row] = (mx, self.pos[row][1])
        else:
            if -hv <= mx:
                x = hv
            else:
                x = -hv
            self.pos[row] = (x, self.pos[row][1])

        if -hv <= my <= hv:
            self.pos[row] = (self.pos[row][0], my)
        else:
            if -hv <= my:
                y = hv
            else:
                y = -hv
            self.pos[row] = (self.pos[row][0], y)

        self.update()


def _set_warning(label: QLabel, warning: bool) -> None:
    """Show a warning sign front of label."""
    warning_icon = "<img width=\"15\" src=\":/icons/warning.png\"/> "
    label.setText(label.text().replace(warning_icon, ''))
    if warning:
        label.setText(warning_icon + label.text())


class ConfigureWidget(QWidget, Ui_Form):

    """Configure widget.

    This interface use to modify structure profile.
    """

    def __init__(
        self,
        add_collection: Callable[[Sequence[Tuple[int, int]]], None],
        parent: MainWindowBase
    ):
        """We need some function from structure collections."""
        super(ConfigureWidget, self).__init__(parent)
        self.setupUi(self)
        self.workbook_no_save = parent.workbook_no_save
        self.get_configure = parent.get_configure
        self.add_collection = add_collection

        # Iteration data
        self.collections: Dict[str, Dict[str, Any]] = {}

        # Customized preview canvas
        self.configure_canvas = _ConfigureCanvas(self)
        self.configure_canvas.set_joint_number.connect(
            self.joint_name.setCurrentIndex
        )
        self.main_layout.insertWidget(0, self.configure_canvas)
        self.main_splitter.setSizes([300, 300])

        self.__clear_panel()

    def add_collections(self, collections: Dict[str, Dict[str, Any]]) -> None:
        """Update the new collections."""
        self.collections.update(collections)

    def clear(self) -> None:
        """Clear all sub-widgets."""
        self.collections.clear()
        self.__clear_panel()

    def __clear_panel(self) -> None:
        """Clear the settings of sub-widgets."""
        self.profile_name.clear()
        self.configure_canvas.clear()
        self.joint_name.clear()
        self.grounded_list.clear()
        self.driver_list.clear()
        self.target_list.clear()
        self.expr_show.clear()
        for label in [
            self.grounded_label,
            self.driver_label,
            self.target_label,
        ]:
            _set_warning(label, True)

    @Slot(name='on_clear_button_clicked')
    def __user_clear(self) -> bool:
        """Ask user before clear."""
        if not self.configure_canvas.G.nodes:
            return True

        if QMessageBox.question(
            self,
            "New profile",
            "Do you want to create a new profile?\n"
            "Unsaved changes will be cleared!"
        ) == QMessageBox.Yes:
            self.__clear_panel()
            return True

        return False

    @Slot(name='on_add_collection_button_clicked')
    def __add_collection(self) -> None:
        """Add the graph back to structure collections."""
        self.add_collection(tuple(self.configure_canvas.G.edges))

    @Slot(Graph, dict)
    def set_graph(
        self,
        graph: Graph,
        pos: Dict[int, _Coord]
    ) -> bool:
        """Set the graph to preview canvas, return False if no clear."""
        if not self.__user_clear():
            return False

        self.configure_canvas.set_graph(graph, pos)

        links: List[List[str]] = [[] for _ in range(len(graph.nodes))]
        for joint, link in edges_view(graph):
            for node in link:
                links[node].append(f'P{joint}')

        for link in links:
            self.grounded_list.addItem("(" + ", ".join(link) + ")")

        # Point name is (P1, P2, P3, ...)
        for node in pos:
            self.joint_name.addItem(f'P{node}')

        return True

    @Slot(int, name='on_grounded_list_currentRowChanged')
    def __set_grounded(self, row: int) -> None:
        """Change current grounded link. Reset all settings."""
        has_choose = row > -1
        _set_warning(self.grounded_label, not has_choose)
        self.configure_canvas.set_grounded(row)
        self.driver_list.clear()
        self.driver_base.clear()
        self.driver_rotator.clear()
        if has_choose:
            item: Optional[QListWidgetItem] = self.grounded_list.item(row)
            if item is None:
                return

            items = item.text().replace('(', '').replace(')', '').split(", ")
            self.driver_base.addItems(items)

        _set_warning(self.driver_label, True)
        if row == self.grounded_list.currentRow():
            return

        self.grounded_list.blockSignals(True)
        self.grounded_list.setCurrentRow(row)
        self.grounded_list.blockSignals(False)

    @Slot(str, name='on_driver_base_currentIndexChanged')
    def __set_driver_base(self, name: str) -> None:
        self.driver_rotator.clear()
        if not name:
            return

        def find_friends(node: int) -> List[str]:
            """Find all the nodes that are same link with input node."""
            ev = dict(edges_view(self.configure_canvas.G))
            link = set(ev[node])
            tmp_list = []
            for node_, link_ in ev.items():
                if node_ == node:
                    continue
                inter = set(link_) & link
                if inter and inter.pop() != self.configure_canvas.grounded:
                    tmp_list.append(f'P{node_}')
            return tmp_list

        self.driver_rotator.addItems(find_friends(int(name.replace('P', ''))))

    @Slot(name='on_driver_add_clicked')
    def __add_driver(self) -> None:
        """Add a input pair."""
        d1 = self.driver_base.currentText()
        d2 = self.driver_rotator.currentText()
        if d1 == d2 == "":
            return

        d1_d2 = f"({d1}, {d2})"
        for n in list_texts(self.driver_list):
            if n == d1_d2:
                return

        self.driver_list.addItem(d1_d2)
        self.__update_driver()
        _set_warning(self.driver_label, False)

    @Slot(name='on_driver_del_clicked')
    def __del_driver(self) -> None:
        """Remove a input pair."""
        row = self.driver_list.currentRow()
        if not row > -1:
            return

        self.driver_list.takeItem(row)
        self.__update_driver()
        _set_warning(self.driver_label, self.driver_list.count() == 0)

    def __update_driver(self) -> None:
        """Update driver for canvas."""
        self.configure_canvas.set_driver([
            eval(s.replace('P', '')) for s in list_texts(self.driver_list)
        ])

    @Slot(name='on_add_customization_clicked')
    def __set_cus_same(self) -> None:
        """Custom points and multiple joints option."""
        dlg = CustomsDialog(self)
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()
        self.configure_canvas.update()

    def __get_current_mechanism_params(self) -> Dict[str, Any]:
        """Get the current mechanism parameters."""
        self.__set_parm_bind()

        input_list = []
        for s in list_texts(self.driver_list):
            pair: Tuple[int, int] = eval(s.replace('P', ''))
            if set(pair) & set(self.configure_canvas.same):
                continue
            input_list.append(pair)

        place_list = {}
        for i in range(self.driver_base.count()):
            joint = int(self.driver_base.itemText(i).replace('P', ''))
            if joint in self.configure_canvas.same:
                continue
            place_list[joint] = None

        target_list = {}
        for s in list_texts(self.target_list):
            target_list[int(s.replace('P', ''))] = None

        return {
            'Expression': self.expr_show.text(),
            'input': input_list,
            'Graph': self.configure_canvas.G.edges,
            'Placement': place_list,
            'Target': target_list,
            'cus': self.configure_canvas.cus.copy(),
            'same': self.configure_canvas.same.copy(),
        }

    @Slot(name='on_load_button_clicked')
    def __from_profile(self) -> None:
        """Show up the dialog to load structure data."""
        dlg = CollectionsDialog(
            self.collections,
            self.get_configure,
            self.workbook_no_save,
            self.configure_canvas.show_ticks,
            self.configure_canvas.monochrome,
            self
        )
        dlg.show()
        if not dlg.exec_():
            dlg.deleteLater()
            return

        # Add customize joints
        params = dlg.params
        graph = Graph(params['Graph'])
        expression: str = params['Expression']
        pos_list = parse_pos(expression)
        cus: Dict[int, int] = params['cus']
        same: Dict[int, int] = params['same']
        for node, ref in sorted(same.items()):
            pos_list.insert(node, pos_list[ref])
        if not self.set_graph(graph, {i: (x, y) for i, (x, y) in enumerate(pos_list)}):
            dlg.deleteLater()
            return

        self.profile_name.setText(dlg.name)
        dlg.deleteLater()
        del dlg
        self.configure_canvas.cus = cus
        self.configure_canvas.same = same

        # Grounded setting
        for row in PreviewCanvas.grounded_detect(set(params['Placement']), graph, same):
            self.__set_grounded(row)

        # Driver, Target
        input_list: List[Tuple[int, int]] = params['input']
        self.driver_list.addItems(f"(P{b}, P{d})" for b, d in input_list)
        self.configure_canvas.set_driver(input_list)
        _set_warning(self.driver_label, self.driver_list.count() == 0)
        target_list: Dict[int, Sequence[_Coord]] = params['Target']
        self.configure_canvas.set_target(target_list)
        self.target_list.addItems(f"P{n}" for n in target_list)
        _set_warning(self.target_label, self.target_list.count() == 0)

        # Expression
        self.expr_show.setText(params['Expression'])

    @Slot(name='on_target_button_clicked')
    def __set_target(self) -> None:
        """Show up target joints dialog."""
        dlg = TargetsDialog(
            "Choose the target points.",
            'P',
            set(self.configure_canvas.pos) - self.configure_canvas.target,
            self.configure_canvas.target,
            self
        )
        dlg.show()
        if not dlg.exec_():
            dlg.deleteLater()
            return

        self.target_list.clear()
        self.target_list.addItems(list_texts(dlg.targets_list))
        self.configure_canvas.set_target(dlg.targets())
        dlg.deleteLater()
        _set_warning(self.target_label, self.target_list.count() == 0)

    @Slot(QListWidgetItem)
    def __set_parm_bind(self, _=None) -> None:
        """Set parameters binding."""
        link_expr_list = []
        for row, gs in enumerate(list_texts(self.grounded_list)):
            try:
                link_expr = []
                # Links from grounded list
                for name in gs.replace('(', '').replace(')', '').split(", "):
                    num = int(name.replace('P', ''))
                    if num in self.configure_canvas.same:
                        name = f'P{self.configure_canvas.same[num]}'
                    link_expr.append(name)
            except KeyError:
                continue
            else:
                # Customize joints
                for joint, link in self.configure_canvas.cus.items():
                    if row == link:
                        link_expr.append(f"P{joint}")
                link_expr_str = ','.join(sorted(set(link_expr)))
                if row == self.grounded_list.currentRow():
                    link_expr_list.insert(0, link_expr_str)
                else:
                    link_expr_list.append(link_expr_str)

        vpoint_exprs = [vpoint.expr() for vpoint in graph2vpoints(
            self.configure_canvas.G,
            self.configure_canvas.pos,
            self.configure_canvas.cus,
            self.configure_canvas.same,
            self.grounded_list.currentRow()
        )]

        self.expr_show.setText("M[" + ", ".join(vpoint_exprs) + "]")

    @Slot(name='on_save_button_clicked')
    def __save(self) -> None:
        """Save the profile to database."""
        if self.profile_name.text():
            name = self.profile_name.text()
            ok = True
        else:
            name, ok = QInputDialog.getText(
                self,
                "Profile name",
                "Please enter the profile name:"
            )
        if not ok:
            return
        i = 0
        while (name not in self.collections) and (not name):
            name = f"Structure_{i}"
        self.collections[name] = self.__get_current_mechanism_params()
        self.profile_name.setText(name)
        self.workbook_no_save()

    @Slot(name='on_clipboard_button_clicked')
    def __copy(self) -> None:
        """Copy the mechanism params."""
        QApplication.clipboard().setText(
            pprint.pformat(self.__get_current_mechanism_params())
        )