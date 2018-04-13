# -*- coding: utf-8 -*-

"""The widget of 'Triangular iteration' tab."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    pyqtSignal,
    QWidget,
    pyqtSlot,
    QMessageBox,
    QInputDialog,
    QListWidgetItem,
    QLabel,
    QApplication,
)
from core.graphics import PreviewCanvas, edges_view
from core.io import get_from_parenthesis, get_front_of_parenthesis
from core.libs import graph_configure
import pprint
from math import sqrt
from networkx import Graph
from typing import (
    Dict,
    List,
    Tuple,
    Set,
    Any
)
from .TriangularIteration_dialog import (
    CollectionsDialog,
    ConstraintsDialog,
    CustomsDialog,
    TargetsDialog,
    SolutionsDialog,
    list_texts,
    list_items,
)
from .Ui_TriangularIteration import Ui_Form

class PreviewWindow(PreviewCanvas):
    
    """Preview window has some functions of mouse interaction."""
    
    set_joint_number = pyqtSignal(int)
    
    def __init__(self, get_solutions_func, parent):
        super(PreviewWindow, self).__init__(get_solutions_func, parent)
        self.pressed = False
        self.get_joint_number = parent.joint_name.currentIndex
    
    def mousePressEvent(self, event):
        """Check if get close to a joint."""
        mx = (event.x() - self.ox) / self.zoom
        my = (event.y() - self.oy) / -self.zoom
        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue
            x = mx - x
            y = my - y
            if sqrt(x*x + y*y) <= 5:
                self.set_joint_number.emit(node)
                self.pressed = True
                break
    
    def mouseReleaseEvent(self, event):
        """Cancel the drag."""
        self.pressed = False
    
    def mouseMoveEvent(self, event):
        """Drag to move the joint."""
        if not self.pressed:
            return
        row = self.get_joint_number()
        if not row>-1:
            return
        mx = (event.x() - self.ox) / self.zoom
        my = (event.y() - self.oy) / -self.zoom
        if -120 <= mx <= 120:
            self.pos[row] = (mx, self.pos[row][1])
        else:
            self.pos[row] = (120 if -120 <= mx else -120, self.pos[row][1])
        if -120 <= my <= 120:
            self.pos[row] = (self.pos[row][0], my)
        else:
            self.pos[row] = (self.pos[row][0], 120 if -120 <= my else -120)
        self.update()

warning_icon = "<img width=\"15\" src=\":/icons/warning.png\"/> "

class CollectionsTriangularIteration(QWidget, Ui_Form):
    
    """Triangular iteration widget."""
    
    def __init__(self, parent=None):
        super(CollectionsTriangularIteration, self).__init__(parent)
        self.setupUi(self)
        self.unsaveFunc = parent.workbookNoSave
        '''
        self.addToCollection = CollectionsStructure.addCollection
        '''
        self.collections = {}
        #Canvas
        self.PreviewWindow = PreviewWindow(
            lambda: tuple(
                self.Expression_list.item(row).text()
                for row in range(self.Expression_list.count())
            ),
            self
        )
        self.PreviewWindow.set_joint_number.connect(
            self.joint_name.setCurrentIndex
        )
        self.main_layout.insertWidget(0, self.PreviewWindow)
        self.show_solutions.clicked.connect(self.PreviewWindow.setShowSolutions)
        #Signals
        self.joint_name.currentIndexChanged.connect(self.__hasSolution)
        self.Expression_list.itemChanged.connect(self.__setParmBind)
        self.clear()
    
    def addCollections(self, collections: Dict[str, Dict[str, Any]]):
        """Update the new collections."""
        self.collections.update(collections)
    
    def clear(self):
        """Clear all sub-widgets."""
        self.collections.clear()
        self.__clearPanel()
    
    def __clearPanel(self):
        """Clear the settings of sub-widgets."""
        self.profile_name = ""
        self.PreviewWindow.clear()
        self.joint_name.clear()
        self.Expression_list.clear()
        self.grounded_list.clear()
        self.Driver_list.clear()
        self.Follower_list.clear()
        self.Target_list.clear()
        self.constraint_list.clear()
        self.Link_Expression.clear()
        self.Expression.clear()
        for label in [
            self.Expression_list_label,
            self.grounded_label,
            self.Driver_label,
            self.Follower_label,
            self.Target_label
        ]:
            self.__setWarning(label, True)
    
    @pyqtSlot()
    def on_clear_button_clicked(self):
        """Ask user before clear."""
        reply = QMessageBox.question(self,
            "New profile",
            "Triangular iteration should be added structure diagrams " +
            "from structure collections.\n" +
            "Do you want to create a new profile?"
        )
        if reply == QMessageBox.Yes:
            self.__clearPanel()
    
    def __setWarning(self, label: QLabel, warning: bool):
        """Show a warning sign front of label."""
        label.setText(label.text().replace(warning_icon, ''))
        if warning:
            label.setText(warning_icon + label.text())
    
    @pyqtSlot()
    def on_addToCollection_button_clicked(self):
        """Add the graph back to structure collections."""
        self.addToCollection(tuple(self.PreviewWindow.G.edges))
    
    @pyqtSlot(Graph, dict)
    def setGraph(self,
        G: Graph,
        pos: Dict[int, Tuple[float, float]]
    ):
        """Set the graph to preview canvas."""
        self.clear()
        self.PreviewWindow.setGraph(G, pos)
        joints = dict(edges_view(G))
        joints_count = set()
        for links in joints.values():
            for link in links:
                joints_count.add(link)
        grounds = [[] for i in range(len(joints_count))]
        for joint, link in joints.items():
            for node in link:
                grounds[node].append(joint)
        for ground in grounds:
            self.grounded_list.addItem("({})".format(", ".join(
                'P{}'.format(node) for node in ground
            )))
        #Point name as (P1, P2, P3, ...).
        for node in pos:
            self.joint_name.addItem('P{}'.format(node))
    
    @pyqtSlot(int)
    def on_grounded_list_currentRowChanged(self, row):
        """Change current grounded linkage."""
        self.__setWarning(self.grounded_label, not row>-1)
        self.PreviewWindow.setGrounded(row)
        self.__hasSolution()
        self.Expression_list.clear()
        self.Expression.clear()
        self.Follower_list.clear()
        self.Driver_list.clear()
        if row > -1:
            self.Follower_list.addItems(
                self.grounded_list.currentItem().text()
                .replace('(', '')
                .replace(')', '')
                .split(", ")
            )
        self.__setWarning(self.Follower_label, not row>-1)
        self.__setWarning(self.Driver_label, True)
        self.__setWarning(self.Expression_list_label, True)
    
    @pyqtSlot(int)
    def __hasSolution(self, index=None):
        """Set buttons enable if there has solution."""
        if index is None:
            index = self.joint_name.currentIndex()
        if not index > -1:
            self.status.setText("N/A")
            self.PLAP_solution.setEnabled(False)
            self.PLLP_solution.setEnabled(False)
            return
        status = self.PreviewWindow.getStatus(index)
        if not status:
            status_str = "Not known."
        elif index in self.PreviewWindow.same:
            status_str = "Same as P{}.".format(self.PreviewWindow.same[index])
        else:
            status_str = "Grounded."
            for expr in list_texts(self.Expression_list):
                if index == int(
                    get_from_parenthesis(expr, '(', ')')
                    .replace('P', '')
                ):
                    status_str = "From {}.".format(
                        get_front_of_parenthesis(expr, '[')
                    )
        self.status.setText(status_str)
        self.PLAP_solution.setEnabled(not status)
        self.PLLP_solution.setEnabled(not status)
    
    @pyqtSlot()
    def on_add_customization_clicked(self):
        """Show up custom joints dialog."""
        dlg = CustomsDialog(self)
        dlg.show()
        dlg.exec_()
        self.PreviewWindow.update()
    
    @pyqtSlot()
    def on_Driver_add_clicked(self):
        """Add a driver joint."""
        row = self.Follower_list.currentRow()
        if not row>-1:
            return
        self.Driver_list.addItem(self.Follower_list.takeItem(row))
        self.PreviewWindow.setDriver([
            int(n.replace('P', '')) for n in list_texts(self.Driver_list)
        ])
        self.__setWarning(self.Driver_label, False)
    
    @pyqtSlot()
    def on_Follower_add_clicked(self):
        """Add a follower joint."""
        row = self.Driver_list.currentRow()
        if not row>-1:
            return
        self.Follower_list.addItem(self.Driver_list.takeItem(row))
        self.__setWarning(self.Driver_label, not bool(self.Driver_list.count()))
    
    def __getCurrentMechanismParams(self) -> Dict[str, Any]:
        """Get the current mechanism parameters."""
        self.__setParmBind()
        return {
            #To keep the origin graph.
            'Graph':tuple(self.PreviewWindow.G.edges),
            #To keep the position of points.
            'pos':self.PreviewWindow.pos.copy(),
            'cus':self.PreviewWindow.cus.copy(),
            'same':self.PreviewWindow.same.copy(),
            #Mechanism params.
            'Driver':{
                s: None for s in list_texts(self.Driver_list)
                if not self.PreviewWindow.isMultiple(s)
            },
            'Follower':{
                s: None for s in list_texts(self.Follower_list)
                if not self.PreviewWindow.isMultiple(s)
            },
            'Target':{
                s: None for s in list_texts(self.Target_list)
            },
            'Link_Expression':self.Link_Expression.text(),
            'Expression':self.Expression.text(),
            'constraint':[tuple(s.split(", ")) for s in list_texts(self.constraint_list)],
        }
    
    @pyqtSlot()
    def on_load_button_clicked(self):
        """Show up the dialog to load structure data."""
        dlg = CollectionsDialog(self)
        dlg.show()
        if not dlg.exec_():
            return
        self.profile_name = dlg.name_loaded
        params = dlg.mechanismParams
        #Add customize joints.
        G = Graph(params['Graph'])
        self.setGraph(G, params['pos'])
        self.PreviewWindow.cus = params['cus']
        self.PreviewWindow.same = params['same']
        #Grounded setting.
        Driver = set(params['Driver'])
        Follower = set(params['Follower'])
        for row, link in enumerate(G.nodes):
            points = set(
                'P{}'.format(n)
                for n, edge in edges_view(G) if link in edge
            )
            if (Driver | Follower) <= points:
                self.grounded_list.setCurrentRow(row)
                break
        #Driver, Follower, Target
        for row in reversed(range(self.Follower_list.count())):
            if self.Follower_list.item(row).text() in Driver:
                self.Follower_list.setCurrentRow(row)
                self.Driver_add.click()
        self.Target_list.addItems(list(params['Target']))
        self.__setWarning(self.Target_label, not self.Target_list.count() > 0)
        #Constraints
        self.constraint_list.addItems([
            ", ".join(c) for c in params['constraint']
        ])
        #Expression
        for expr in params['Expression'].split(';'):
            item = QListWidgetItem()
            self.Expression_list.addItem(item)
            item.setText(expr)
            self.PreviewWindow.setStatus(get_from_parenthesis(expr, '(', ')'), True)
        self.__setWarning(
            self.Expression_list_label,
            not self.PreviewWindow.isAllLock()
        )
    
    @pyqtSlot()
    def on_constraints_button_clicked(self):
        """Show up constraint dialog."""
        dlg = ConstraintsDialog(self)
        dlg.show()
        if not dlg.exec_():
            return
        self.constraint_list.clear()
        for constraint in list_texts(dlg.main_list):
            self.constraint_list.addItem(constraint)
    
    @pyqtSlot()
    def on_Target_button_clicked(self):
        """Show up target joints dialog."""
        dlg = TargetsDialog(self)
        dlg.show()
        if not dlg.exec_():
            return
        self.Target_list.clear()
        for target in list_texts(dlg.targets_list):
            self.Target_list.addItem(target)
        self.__setWarning(self.Target_label, not self.Target_list.count()>0)
    
    def __symbols(self) -> Set[List[str]]:
        """Return all symbols."""
        expr_list = set([])
        for expr in self.Expression.text().split(';'):
            param_list = get_from_parenthesis(expr, '[', ']').split(',')
            param_list.append(get_from_parenthesis(expr, '(', ')'))
            expr_list.update(param_list)
        return expr_list
    
    def __getParam(self, angle: bool =False) -> int:
        """Get the link / angle parameter number."""
        i = 0
        p = '{}{{}}'.format('a' if angle else 'L')
        while p.format(i) in self.__symbols():
            i += 1
        return i
    
    @pyqtSlot()
    def on_PLAP_solution_clicked(self):
        """Show up dialog to add a PLAP solution."""
        dlg = SolutionsDialog('PLAP', self)
        dlg.show()
        if not dlg.exec_():
            return
        point = self.joint_name.currentText()
        self.__addSolution(
            "PLAP",
            dlg.point_A.currentText(),
            'L{}'.format(self.__getParam()),
            'a{}'.format(self.__getParam(angle=True)),
            dlg.point_B.currentText(),
            point
        )
    
    @pyqtSlot()
    def on_PLLP_solution_clicked(self):
        """Show up dialog to add a PLLP solution."""
        dlg = SolutionsDialog('PLLP', self)
        dlg.show()
        if not dlg.exec_():
            return
        point = self.joint_name.currentText()
        link_num = self.__getParam()
        self.__addSolution(
            "PLLP",
            dlg.point_A.currentText(),
            'L{}'.format(link_num),
            'L{}'.format(link_num + 1),
            dlg.point_B.currentText(),
            point
        )
    
    def __addSolution(self, *expr: Tuple[str]):
        """Add a solution."""
        item = QListWidgetItem()
        self.Expression_list.addItem(item)
        item.setText("{}[{}]({})".format(expr[0], ','.join(expr[1:-1]), expr[-1]))
        self.PreviewWindow.setStatus(expr[-1], True)
        self.__hasSolution()
        self.__setWarning(
            self.Expression_list_label,
            not self.PreviewWindow.isAllLock()
        )
    
    @pyqtSlot(QListWidgetItem)
    def __setParmBind(self, item=None):
        """Set parameters binding."""
        self.Expression.setText(';'.join(list_texts(self.Expression_list)))
        link_expr_list = []
        for row, gs in list_texts(self.grounded_list, True):
            try:
                link_expr = []
                #Links from grounded list.
                for name in gs.replace('(', '').replace(')', '').split(", "):
                    if self.PreviewWindow.isMultiple(name):
                        name = 'P{}'.format(
                            self.PreviewWindow.same[int(name.replace('P', ''))]
                        )
                    link_expr.append(name)
            except KeyError:
                continue
            else:
                #Customize joints.
                for joint, link in self.PreviewWindow.cus.items():
                    if row==link:
                        link_expr.append(joint)
                link_expr_str = ','.join(sorted(set(link_expr)))
                if row==self.grounded_list.currentRow():
                    link_expr_list.insert(0, link_expr_str)
                else:
                    link_expr_list.append(link_expr_str)
        self.Link_Expression.setText(';'.join(
            ('ground' if i==0 else '') + "[{}]".format(link)
            for i, link in enumerate(link_expr_list)
        ))
    
    @pyqtSlot()
    def on_Expression_auto_clicked(self):
        """Auto configure the solutions."""
        if not self.Driver_list.count():
            QMessageBox.information(self,
                "Auto configure",
                "Please setting the driver joint(s)."
            )
            return
        reply = QMessageBox.question(self,
            "Auto configure",
            "This function can detect the structure " +
            "to configure the solutions.\n" +
            "The current settings will be cleared."
        )
        if (
            (reply != QMessageBox.Yes) or
            (not self.on_Expression_clear_clicked())
        ):
            return
        exprs = graph_configure(
            self.PreviewWindow.G,
            self.PreviewWindow.status,
            self.PreviewWindow.pos,
            [item.text() for item in list_items(self.Driver_list)],
            self.PreviewWindow.cus,
            self.PreviewWindow.same,
        )
        for expr in exprs:
            item = QListWidgetItem()
            self.Expression_list.addItem(item)
            item.setText(
                "{}[{}]({})".format(expr[0], ','.join(expr[1:-1]), expr[-1])
            )
        self.__hasSolution()
        self.__setWarning(
            self.Expression_list_label,
            not self.PreviewWindow.isAllLock()
        )
        self.PreviewWindow.update()
    
    @pyqtSlot()
    def on_Expression_pop_clicked(self):
        """Remove the last solution."""
        count = self.Expression_list.count()
        if not count:
            return
        expr = self.Expression_list.item(count-1).text()
        self.Expression_list.takeItem(count-1)
        self.PreviewWindow.setStatus(
            get_from_parenthesis(expr, '(', ')'),
            False
        )
        self.__setParmBind()
    
    @pyqtSlot()
    def on_Expression_clear_clicked(self) -> bool:
        """Clear the solutions. Return true if success."""
        if not self.Expression_list.count():
            return True
        reply = QMessageBox.question(self,
            "Clear the solutions",
            "Are you sure to clear the solutions?"
        )
        if reply != QMessageBox.Yes:
            return False
        self.PreviewWindow.setGrounded(self.grounded_list.currentRow())
        self.Expression_list.clear()
        self.Expression.clear()
        self.__hasSolution()
        return True
    
    @pyqtSlot()
    def on_save_button_clicked(self):
        """Save the profile to database."""
        if self.profile_name:
            name = self.profile_name
            ok = True
        else:
            name, ok = QInputDialog.getText(self,
                "Profile name",
                "Please enter the profile name:"
            )
        if not ok:
            return
        i = 0
        while (name not in self.collections) and (not name):
            name = "Structure_{}".format(i)
        self.collections[name] = self.__getCurrentMechanismParams()
        self.profile_name = name
        self.unsaveFunc()
    
    @pyqtSlot()
    def on_clipboard_button_clicked(self):
        """Copy the mechanism params."""
        QApplication.clipboard().setText(
            pprint.pformat(self.__getCurrentMechanismParams())
        )
