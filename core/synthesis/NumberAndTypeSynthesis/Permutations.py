# -*- coding: utf-8 -*-

from ...QtModules import *
from .Ui_Permutations import Ui_Form

class Permutations_show(QWidget, Ui_Form):
    def __init__(self, jointDataFunc, linkDataFunc, dofFunc, parent=None):
        super(Permutations_show, self).__init__(parent)
        self.setupUi(self)
        self.jointDataFunc = jointDataFunc
        self.linkDataFunc = linkDataFunc
        self.dofFunc = dofFunc
        self.Representation_tree.expanded.connect(self.resizeHeader)
        self.Representation_tree.collapsed.connect(self.resizeHeader)
    
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        dof = self.dofFunc()
        self.Representation_joint.setText("M[{}]".format(", ".join(str(vpoint) for vpoint in jointData)))
        self.Representation_link.setText("M[{}]".format(", ".join(str(vlink) for vlink in linkData)))
        self.Representation_tree.clear()
        #Show mechanism system.
        root = QTreeWidgetItem(["Mechanism root"])
        self.Representation_tree.addTopLevelItem(root)
        root.addChildren([
            QTreeWidgetItem(["Degree of freedom", str(dof)]),
            QTreeWidgetItem(["Number of links", str(len(tuple(None for vlink in linkData if len(vlink.points)>1)))]),
            QTreeWidgetItem(["Number of joints", str(len(tuple(None for vpoint in jointData if len(vpoint.links)>1)))]),
        ])
        for vlink in linkData:
            node = QTreeWidgetItem([vlink.name])
            root.addChild(node)
            node.addChild(QTreeWidgetItem(["Number of joints", str(sum(len(jointData[i].links)-1 for i in vlink.points))]))
            node.addChildren([
                QTreeWidgetItem(["Point{}".format(i), ", ".join(link for link in jointData[i].links if link!=vlink.name)])
                for i in vlink.points
            ])
            self.Representation_tree.expandItem(node)
        self.Representation_tree.expandItem(root)
    
    @pyqtSlot(QModelIndex)
    def resizeHeader(self, index=None):
        for i in range(self.Representation_tree.columnCount()):
            self.Representation_tree.resizeColumnToContents(i)
