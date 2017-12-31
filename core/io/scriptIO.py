# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from ..QtModules import *
from ..info.info import VERSION
from .Ui_script import Ui_Info_Dialog

script_title = '''\
#This script is generate by Pyslvs {}.

from math import (
    radians,
    sqrt,
    cos,
    sin
)
from slvs import (
    #System base
    System, groupNum, Slvs_MakeQuaternion,
    #Entities & Constraint
    Point3d, Workplane, Normal3d, Point2d, LineSegment2d, Constraint,
    #Result flags
    SLVS_RESULT_OKAY, SLVS_RESULT_INCONSISTENT, SLVS_RESULT_DIDNT_CONVERGE, SLVS_RESULT_TOO_MANY_UNKNOWNS
)

class VPoint:
    __slots__ = ('links', 'type', 'angle', '__c')
    
    def __init__(self, links, type, angle, c):
        self.links = links
        self.type = type
        self.angle = angle
        self.__c = c
    
    @property
    def cx(self):
        return self.__c[0][0]
    
    @property
    def cy(self):
        return self.__c[0][1]
    
    @property
    def c(self):
        return self.__c
    
    def distance(self, p):
        return round(sqrt((self.cx-p.cx)**2 + (self.cy-p.cy)**2), 4)

class VLink:
    __slots__ = ('name', 'points')
    
    def __init__(self, name, points):
        self.name = name
        self.points = points

class SlvsException(Exception):
    pass

def slvsProcess(Point, Link, constraints):
    pointCount = sum([len(vpoint.c) for vpoint in Point])
    sliderCount = sum([1 for vpoint in Point if vpoint.type==1 or vpoint.type==2])
    constraintCount = len(constraints)
    Sys = System(pointCount*2 + sliderCount*2 + constraintCount*2 + 12)
    Sys.default_group = groupNum(1)
    p0 = Sys.add_param(0.)
    p1 = Sys.add_param(0.)
    p2 = Sys.add_param(0.)
    Origin = Point3d(p0, p1, p2)
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = Sys.add_param(qw)
    p4 = Sys.add_param(qx)
    p5 = Sys.add_param(qy)
    p6 = Sys.add_param(qz)
    Workplane1 = Workplane(Origin, Normal3d(p3, p4, p5, p6))
    p7 = Sys.add_param(0.)
    p8 = Sys.add_param(0.)
    Origin2D = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Origin2D)
    p9 = Sys.add_param(10.)
    p10 = Sys.add_param(0.)
    hp = Point2d(Workplane1, p9, p10)
    Constraint.dragged(Workplane1, hp)
    #Name 'ground' is a horizontal line through (0, 0).
    ground = LineSegment2d(Workplane1, Origin2D, hp)
    Sys.default_group = groupNum(2)
    Slvs_Points = []
    #Append all points first.
    for vpoint in Point:
        #This is the point recorded in the table.
        if vpoint.type==0:
            #Has only one coordinate
            Slvs_Points.append(Point2d(Workplane1, Sys.add_param(vpoint.cx), Sys.add_param(vpoint.cy)))
        elif vpoint.type==1 or vpoint.type==2:
            #Has one more pointer
            Slvs_Points.append(
                tuple(Point2d(Workplane1, Sys.add_param(cx), Sys.add_param(cy)) for cx, cy in vpoint.c)
            )
    #Topology of PMKS points.
    LinkIndex = lambda l: [vlink.name for vlink in Link].index(l)
    for i, vpoint in enumerate(Point):
        #P and RP Joint: If the point has a sliding degree of freedom.
        if vpoint.type==1 or vpoint.type==2:
            #Make auxiliary line as a slider slot (The length is 10.0).
            p_base = Slvs_Points[i][0]
            p_assist = Point2d(Workplane1,
                Sys.add_param(vpoint.cx + 10.*cos(radians(vpoint.angle))),
                Sys.add_param(vpoint.cy + 10.*sin(radians(vpoint.angle)))
            )
            l_slot = LineSegment2d(Workplane1, p_base, p_assist)
            Constraint.distance(10., Workplane1, p_base, p_assist)
            #Angle constraint function:
            def relateWith(linkName):
                if linkName=='ground':
                    #Angle can not be zero.
                    if vpoint.angle==0. or vpoint.angle==180.:
                        Constraint.parallel(Workplane1, ground, l_slot)
                    else:
                        Constraint.angle(Workplane1, vpoint.angle, ground, l_slot)
                else:
                    relate = Link[LinkIndex(linkName)].points
                    relateNum = relate[relate.index(i)-1]
                    relate_vpoint = Point[relateNum]
                    p_main = Slvs_Points[i][vpoint.links.index(linkName)]
                    if relate_vpoint.type==1 or relate_vpoint.type==2:
                        p_link_assist = Slvs_Points[relateNum][relate_vpoint.links.index(linkName)]
                    else:
                        p_link_assist = Slvs_Points[relateNum]
                    l_link = LineSegment2d(Workplane1, p_main, p_link_assist)
                    angle_base = vpoint.slopeAngle(relate_vpoint)
                    if angle_base==0. or angle_base==180.:
                        Constraint.parallel(Workplane1, l_link, l_slot)
                    else:
                        Constraint.angle(Workplane1, angle_base, l_link, l_slot)
            #The slot has an angle with base link.
            relateWith(vpoint.links[0])
            #All point should on the slot.
            for p in Slvs_Points[i][1:]:
                Constraint.on(Workplane1, p, l_slot)
            #P Joint: The point do not have freedom of rotation.
            if vpoint.type==1:
                for linkName in vpoint.links[1:]:
                    relateWith(linkName)
        #Link to other points on the same link.
        for linkOrder, linkName in enumerate(vpoint.links):
            #If the joint is a slider, defined its base.
            if vpoint.type==1 or vpoint.type==2:
                p_base = Slvs_Points[i][linkOrder]
            else:
                p_base = Slvs_Points[i]
            #If this link is on the ground.
            if linkName=='ground':
                Constraint.dragged(Workplane1, p_base)
                continue
            relate = Link[LinkIndex(linkName)].points
            relateOrder = relate.index(i)
            #Pass if this is the first point.
            if relateOrder==0:
                continue
            #Connect function, and return the distance.
            def getConnection(index: int):
                n = relate[index]
                p = Point[n]
                d = p.distance(vpoint)
                if p.type==1 or p.type==2:
                    p_contact = Slvs_Points[n][p.links.index(linkName)]
                else:
                    p_contact = Slvs_Points[n]
                return (d, p_contact)
            def ConnectTo(d, p_contact):
                if d:
                    Constraint.distance(d, Workplane1, p_base, p_contact)
                else:
                    Constraint.on(Workplane1, p_base, p_contact)
            #Connection of the first point in this link.
            connect_1 = getConnection(0)
            if relateOrder>1:
                #Conection of the previous point.
                connect_2 = getConnection(relateOrder-1)
                if bool(connect_1[0])!=bool(connect_2[0]):
                    #Same point. Just connect to same point.
                    ConnectTo(*(connect_1 if connect_1[0]==0. else connect_2))
                elif min(
                    abs(2*connect_1[0]-connect_2[0]),
                    abs(connect_1[0]-2*connect_2[0]),
                ) < 0.01:
                    #Collinear.
                    Constraint.on(Workplane1, p_base, LineSegment2d(Workplane1, connect_1[1], connect_2[1]))
                    ConnectTo(*connect_1)
                else:
                    #Normal status.
                    ConnectTo(*connect_1)
                    ConnectTo(*connect_2)
            else:
                ConnectTo(*connect_1)
    #The constraints of drive shaft.
    for shaft, base_link, drive_link, angle in constraints:
        #Base point as shaft center.
        if Point[shaft].type!=0:
            p_base = Slvs_Points[shaft][0]
        else:
            p_base = Slvs_Points[shaft]
        #Base link slope angle.
        if base_link!='ground':
            relate_base = Link[LinkIndex(base_link)].points
            newRelateOrder_base = relate_base.index(shaft)-1
            angle -= Point[shaft].slopeAngle(Point[newRelateOrder_base])
            angle %= 360.
        x = Sys.add_param(round(Point[shaft].cx + 10.*cos(radians(angle)), 8))
        y = Sys.add_param(round(Point[shaft].cy + 10.*sin(radians(angle)), 8))
        p_hand = Point2d(Workplane1, x, y)
        Constraint.dragged(Workplane1, p_hand)
        #The virtual link that dragged by "hand".
        leader = LineSegment2d(Workplane1, p_base, p_hand)
        #Make another virtual link that should follow "hand".
        relate_drive = Link[LinkIndex(drive_link)].points
        newRelateOrder_drive = relate_drive[relate_drive.index(shaft)-1]
        if Point[newRelateOrder_drive].type!=0:
            p_drive = Slvs_Points[newRelateOrder_drive][0]
        else:
            p_drive = Slvs_Points[newRelateOrder_drive]
        link = LineSegment2d(Workplane1, p_base, p_drive)
        Constraint.angle(Workplane1, .5, link, leader)
    #Solve
    result_flag = Sys.solve()
    if result_flag==SLVS_RESULT_OKAY:
        resultList = []
        for p in Slvs_Points:
            if type(p)==Point2d:
                resultList.append((round(p.u().value, 4), round(p.v().value, 4)))
            else:
                resultList.append(tuple((round(c.u().value, 4), round(c.v().value, 4)) for c in p))
        return resultList, int(Sys.dof)
    else:
        if result_flag==SLVS_RESULT_INCONSISTENT:
            error = "Inconsistent."
        elif result_flag==SLVS_RESULT_DIDNT_CONVERGE:
            error = "Did not converge."
        elif result_flag==SLVS_RESULT_TOO_MANY_UNKNOWNS:
            error = "Too many unknowns."
        raise SlvsException(error)

if __name__=="__main__":
    Point = {}
    Link = {}
    """
    constraints = (
        (
            "Point number": int,
            "Base link name": str,
            "Drive link name": str,
            "Angle (degrees)": float
        ),
    )
    """
    constraints = ()
    print("Coordinates: {{}}\\nDOF: {{}}".format(*slvsProcess(Point, Link, constraints)))
'''

def slvsProcessScript(VPointList, VLinkList):
    return script_title.format(
        "v{}.{}.{} ({})".format(*VERSION),
        [vpoint for vpoint in VPointList],
        [vlink for vlink in VLinkList]
    )

class highlightRule:
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format

class keywordSyntax(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(keywordSyntax, self).__init__(parent)
        keyword = QTextCharFormat()
        keyword.setForeground(QBrush(Qt.darkBlue, Qt.SolidPattern))
        keyword.setFontWeight(QFont.Bold)
        number = QTextCharFormat()
        number.setForeground(QBrush(QColor(0, 127, 127), Qt.SolidPattern))
        annotation = QTextCharFormat()
        annotation.setForeground(QBrush(QColor(61, 158, 77), Qt.SolidPattern))
        decorator = QTextCharFormat()
        decorator.setForeground(QBrush(QColor(158, 140, 61), Qt.SolidPattern))
        function = QTextCharFormat()
        function.setFontWeight(QFont.Bold)
        function.setForeground(QBrush(QColor(10, 147, 111), Qt.SolidPattern))
        string = QTextCharFormat()
        string.setForeground(QBrush(QColor(127, 0, 127), Qt.SolidPattern))
        boolean = QTextCharFormat()
        boolean.setForeground(QBrush(QColor(64, 112, 144), Qt.SolidPattern))
        self.highlightingRules = [
            highlightRule(QRegExp(r'\b[+-]?[0-9]+[lL]?\b'), number),
            highlightRule(QRegExp(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b'), number),
            highlightRule(QRegExp(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b'), number),
            highlightRule(QRegExp(r'\bdef\b\s*(\w+)'), function),
            highlightRule(QRegExp(r'\bclass\b\s*(\w+)'), function)
        ]
        self.highlightingRules += [
            highlightRule(QRegExp("\\b"+key+"\\b"), keyword) for key in
            ['print', 'pass', 'def', 'class', 'from', 'is', 'as', 'import', 'for', 'in', 'if', 'else', 'elif', 'raise']
        ]
        self.highlightingRules += [highlightRule(QRegExp("\\b"+key+"\\b"), boolean) for key in ['self', 'True', 'False']]
        self.highlightingRules += [
            highlightRule(QRegExp("'''"), string),
            highlightRule(QRegExp('"""'), string),
            highlightRule(QRegExp(r'"[^"\\]*(\\.[^"\\]*)*"'), string),
            highlightRule(QRegExp(r"'[^'\\]*(\\.[^'\\]*)*'"), string),
            highlightRule(QRegExp(r'@[^(\n|\()]*'), decorator),
            highlightRule(QRegExp(r'#[^\n]*'), annotation)
        ]
    
    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index>=0:
              length = expression.matchedLength()
              self.setFormat(index, length, rule.format)
              index = text.find(expression.pattern(), index+length)
        self.setCurrentBlockState(0)

class highlightTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(highlightTextEdit, self).__init__(parent)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setStyleSheet("font: 10pt \"Bitstream Vera Sans Mono\";")
        keywordSyntax(self)
    
class Script_Dialog(QDialog, Ui_Info_Dialog):
    def __init__(self, Point, Line, parent):
        super(Script_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.script = highlightTextEdit()
        self.verticalLayout.insertWidget(1, self.script)
        self.script.setPlainText(slvsProcessScript(Point, Line))
    
    @pyqtSlot()
    def on_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.script.toPlainText())
        self.copy.setText("Copied!")
    
    @pyqtSlot()
    def on_save_clicked(self):
        fileName = self.outputTo("Python script", ["Python3 Script(*.py)"])
        if fileName:
            with open(fileName, 'w', newline="") as f:
                f.write(self.script.toPlainText())
            self.saveReplyBox("Python script", fileName)
