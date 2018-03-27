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
import pprint
from math import sqrt
from networkx import Graph
from string import ascii_uppercase
from itertools import product
from typing import (
    Dict,
    List,
    Tuple,
    Sequence,
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
    combo_texts,
    list_items,
)
from .Ui_TriangularIteration import Ui_Form

def letter_names():
    """This is a generator to get a
    non-numeric and non-repeat name string.
    
    ('A', 'B', ..., 'AA', 'AB', ..., 'AAA', 'AAB', ...)
    """
    i = 0
    while True:
        i += 1
        for e in product(ascii_uppercase, repeat=i):
            yield ''.join(e)

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
    
    def friends(self, node1: int, reliable: bool =False) -> int:
        """Return a generator yield the nodes
        that has solution on the same link.
        """
        #All edges of all nodes.
        edges = dict(edges_view(self.G))
        for n, l in self.cus.items():
            edges[int(n.replace('P', ''))] = (l,)
        #Reverse dict of 'self.same'.
        same_r = {v: k for k, v in self.same.items()}
        #for all link of node1.
        links1 = set(edges[node1])
        if node1 in same_r:
            links1.update(edges[same_r[node1]])
        #for all link.
        for node2 in edges:
            if (node1 == node2) or (node2 in self.same):
                continue
            links2 = set(edges[node2])
            if node2 in same_r:
                links2.update(edges[same_r[node2]])
            #Reference by intersection and status.
            if (links1 & links2) and (not self.getStatus(node2) != reliable):
                yield node2
    
    def sort_nodes(self, nodes: Sequence[int]):
        """Sort the nodes by x value of position."""
        return sorted(nodes, key=lambda n: self.pos[n][0], reverse=True)

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
        self.parm_bind = {}
        #Canvas
        self.PreviewWindow = PreviewWindow(
            lambda: tuple(
                self.Expression_list.item(row).text()
                for row in range(self.Expression_list.count())
            ),
            self
        )
        self.PreviewWindow.set_joint_number.connect(self.joint_name.setCurrentIndex)
        self.main_layout.insertWidget(0, self.PreviewWindow)
        self.show_solutions.clicked.connect(self.PreviewWindow.setShowSolutions)
        #Signals
        self.joint_name.currentIndexChanged.connect(self.hasSolution)
        self.Expression_list.itemChanged.connect(self.set_parm_bind)
        self.clear()
    
    def addCollections(self, collections: Dict[str, Dict[str, Any]]):
        """Update the new collections."""
        self.collections.update(collections)
    
    def clear(self):
        """Clear all sub-widgets."""
        self.collections.clear()
        self.clearPanel()
    
    def clearPanel(self):
        """Clear the settings of sub-widgets."""
        self.profile_name = ""
        self.PreviewWindow.clear()
        self.joint_name.clear()
        self.Expression_list.clear()
        self.parm_bind.clear()
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
            self.setWarning(label, True)
    
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
            self.clearPanel()
    
    def setWarning(self, label: QLabel, warning: bool):
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
        self.setWarning(self.grounded_label, not row>-1)
        self.PreviewWindow.setGrounded(row)
        self.hasSolution()
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
        self.setWarning(self.Follower_label, not row>-1)
        self.setWarning(self.Driver_label, True)
        self.setWarning(self.Expression_list_label, True)
    
    @pyqtSlot(int)
    def hasSolution(self, index=None):
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
        self.setWarning(self.Driver_label, False)
    
    @pyqtSlot()
    def on_Follower_add_clicked(self):
        """Add a follower joint."""
        row = self.Driver_list.currentRow()
        if not row>-1:
            return
        self.Follower_list.addItem(self.Driver_list.takeItem(row))
        self.setWarning(self.Driver_label, not bool(self.Driver_list.count()))
    
    def symbols(self) -> Set[List[str]]:
        """Return all symbols."""
        expr_list = set([])
        for expr in self.Expression.text().split(';'):
            param_list = get_from_parenthesis(expr, '[', ']').split(',')
            param_list.append(get_from_parenthesis(expr, '(', ')'))
            expr_list.update(param_list)
        return expr_list
    
    def getParam(self, angle: bool =False) -> int:
        """Get the link / angle parameter number."""
        i = 0
        p = '{}{{}}'.format('a' if angle else 'L')
        while p.format(i) in self.symbols():
            i += 1
        return i
    
    def get_currentMechanismParams(self) -> Dict[str, Any]:
        """Get the current mechanism parameters."""
        self.set_parm_bind()
        return {
            #To keep the origin graph.
            'Graph':tuple(self.PreviewWindow.G.edges),
            #To keep the position of points.
            'pos':self.PreviewWindow.pos.copy(),
            'cus':self.PreviewWindow.cus.copy(),
            'same':self.PreviewWindow.same.copy(),
            'name_dict':{v:k for k, v in self.parm_bind.items()},
            #Mechanism params.
            'Driver':{
                self.parm_bind[s]:None for s in list_texts(self.Driver_list)
                if not self.PreviewWindow.isMultiple(s)
            },
            'Follower':{
                self.parm_bind[s]:None for s in list_texts(self.Follower_list)
                if not self.PreviewWindow.isMultiple(s)
            },
            'Target':{
                self.parm_bind[s]:None for s in list_texts(self.Target_list)
            },
            'Link_Expression':self.Link_Expression.text(),
            'Expression':self.Expression.text(),
            'constraint':[tuple(
                self.parm_bind[name] for name in s.split(", ")
            ) for s in list_texts(self.constraint_list)]
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
        mapping = params['name_dict']
        #Add customize joints.
        G = Graph(params['Graph'])
        self.setGraph(G, params['pos'])
        self.PreviewWindow.cus = params['cus']
        self.PreviewWindow.same = params['same']
        #Grounded setting.
        Driver = [mapping[e] for e in params['Driver']]
        Follower = [mapping[e] for e in params['Follower']]
        for row, link in enumerate(G.nodes):
            points = set(
                'P{}'.format(n)
                for n, edge in edges_view(G) if link in edge
            )
            if set(Driver + Follower) <= points:
                self.grounded_list.setCurrentRow(row)
                break
        #Driver, Follower, Target
        for row in reversed(range(self.Follower_list.count())):
            if self.Follower_list.item(row).text() in Driver:
                self.Follower_list.setCurrentRow(row)
                self.Driver_add.click()
        self.Target_list.addItems([mapping[e] for e in params['Target']])
        self.setWarning(self.Target_label, not self.Target_list.count()>0)
        #Constraints
        self.constraint_list.addItems([
            ", ".join(mapping[e] for e in c) for c in params['constraint']
        ])
        #Expression
        for expr in params['Expression'].split(';'):
            params = get_from_parenthesis(expr, '[', ']').split(',')
            target = get_from_parenthesis(expr, '(', ')')
            params.append(target)
            for p in params:
                try:
                    #Try to avoid replace function name.
                    expr = mapping[p].join(expr.rsplit(p, 1))
                except KeyError:
                    continue
            item = QListWidgetItem()
            self.Expression_list.addItem(item)
            item.setText(expr)
            self.PreviewWindow.setStatus(mapping[target], True)
        self.setWarning(self.Expression_list_label, not self.PreviewWindow.isAllLock())
    
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
        self.setWarning(self.Target_label, not self.Target_list.count()>0)
    
    @pyqtSlot()
    def on_PLAP_solution_clicked(self):
        """Show up dialog to add a PLAP solution."""
        dlg = SolutionsDialog('PLAP', self)
        dlg.show()
        if not dlg.exec_():
            return
        point = self.joint_name.currentText()
        self.addSolution(point, (
            "PLAP",
            dlg.point_A.currentText(),
            'L{}'.format(self.getParam()),
            'a{}'.format(self.getParam(angle=True)),
            dlg.point_B.currentText(),
            point
        ))
    
    @pyqtSlot()
    def on_PLLP_solution_clicked(self):
        """Show up dialog to add a PLLP solution."""
        dlg = SolutionsDialog('PLLP', self)
        dlg.show()
        if not dlg.exec_():
            return
        point = self.joint_name.currentText()
        link_num = self.getParam()
        self.addSolution(point, (
            "PLLP",
            dlg.point_A.currentText(),
            'L{}'.format(link_num),
            'L{}'.format(link_num + 1),
            dlg.point_B.currentText(),
            point
        ))
    
    def addSolution(self, point: str, expr: Tuple[str]):
        """Add a solution."""
        item = QListWidgetItem()
        self.Expression_list.addItem(item)
        item.setText("{}[{},{},{},{}]({})".format(*expr))
        self.PreviewWindow.setStatus(point, True)
        self.hasSolution()
        self.setWarning(self.Expression_list_label, not self.PreviewWindow.isAllLock())
    
    @pyqtSlot(QListWidgetItem)
    def set_parm_bind(self, item=None):
        """Set parameters binding."""
        self.parm_bind.clear()
        expr_list = []
        #At this time, we should turn the points number to letter names.
        ln = letter_names()
        #Set functional expression.
        for expr in list_texts(self.Expression_list):
            params = get_from_parenthesis(expr, '[', ']').split(',')
            params.append(get_from_parenthesis(expr, '(', ')'))
            for name in params:
                if 'P' in name:
                    #Find out with who was shown earlier.
                    if name not in self.parm_bind:
                        self.parm_bind[name] = next(ln)
                    expr = expr.replace(name, self.parm_bind[name])
            expr_list.append(expr)
        #If there has any joints not named yet.
        for name in combo_texts(self.joint_name):
            if name not in self.parm_bind:
                self.parm_bind[name] = next(ln)
        #Set link expression.
        link_expr_list = []
        self.Expression.setText(';'.join(expr_list))
        for row, gs in list_texts(self.grounded_list, True):
            try:
                link_expr = []
                #Links from grounded list.
                for name in gs.replace('(', '').replace(')', '').split(", "):
                    if self.PreviewWindow.isMultiple(name):
                        name = 'P{}'.format(self.PreviewWindow.same[int(name.replace('P', ''))])
                    link_expr.append(self.parm_bind[name])
            except KeyError:
                continue
            else:
                #Customize joints.
                for joint, link in self.PreviewWindow.cus.items():
                    if row==link:
                        link_expr.append(self.parm_bind[joint])
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
            "This function can detect the structure to configure the solutions.\n" +
            "The current settings will be cleared."
        )
        if reply == QMessageBox.Yes and self.on_Expression_clear_clicked():
            self.auto_configure_expression()
    
    def auto_configure_expression(self):
        """Auto configuration algorithm."""
        friends = self.PreviewWindow.friends
        sort_nodes = self.PreviewWindow.sort_nodes
        #PLAP solutions.
        for item in list_items(self.Driver_list):
            node = int(item.text().replace('P', ''))
            point1 = 'P{}'.format(node)
            point2 = 'P{}'.format(next(friends(node)))
            self.addSolution(point2, (
                "PLAP",
                point1,
                'L{}'.format(self.getParam()),
                'a{}'.format(self.getParam(angle=True)),
                'P{}'.format(sort_nodes(friends(node, reliable=True))[0]),
                point2
            ))
        #PLLP solutions.
        node = 0
        while not self.PreviewWindow.isAllLock():
            if node not in self.PreviewWindow.pos:
                node = 0
                continue
            status = self.PreviewWindow.getStatus(node)
            #Set the solution.
            if status:
                node += 1
                continue
            rf = friends(node, reliable=True)
            try:
                two_friend = sort_nodes((next(rf), next(rf)))
            except StopIteration:
                pass
            else:
                #Add solution.
                link_num = self.getParam()
                point = 'P{}'.format(node)
                self.addSolution(point, (
                    "PLLP",
                    'P{}'.format(two_friend[0]),
                    'L{}'.format(link_num),
                    'L{}'.format(link_num + 1),
                    'P{}'.format(two_friend[1]),
                    point
                ))
            node += 1
    
    @pyqtSlot()
    def on_Expression_pop_clicked(self):
        """Remove the last solution."""
        count = self.Expression_list.count()
        if not count:
            return
        expr = self.Expression_list.item(count-1).text()
        self.Expression_list.takeItem(count-1)
        self.PreviewWindow.setStatus(get_from_parenthesis(expr, '(', ')'), False)
        self.set_parm_bind()
    
    @pyqtSlot()
    def on_Expression_clear_clicked(self) -> bool:
        """Clear the solutions. Return true if success."""
        if not self.Expression_list.count():
            return True
        reply = QMessageBox.question(self,
            "Clear the solutions",
            "Are you sure to clear the solutions?"
        )
        if reply == QMessageBox.Yes:
            self.PreviewWindow.setGrounded(self.grounded_list.currentRow())
            self.Expression_list.clear()
            self.Expression.clear()
            self.hasSolution()
        return reply == QMessageBox.Yes
    
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
        if ok:
            i = 0
            while (name not in self.collections) and (not name):
                name = "Structure_{}".format(i)
            self.collections[name] = self.get_currentMechanismParams()
            self.profile_name = name
            self.unsaveFunc()
    
    @pyqtSlot()
    def on_clipboard_button_clicked(self):
        """Copy the mechanism params."""
        QApplication.clipboard().setText(
            pprint.pformat(self.get_currentMechanismParams())
        )
