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
from .scriptType import slvsProcessScript
tr = QCoreApplication.translate
from .Ui_script import Ui_Info_Dialog

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
        commit = QTextCharFormat()
        commit.setForeground(QBrush(QColor(127, 0, 0), Qt.SolidPattern))
        string = QTextCharFormat()
        string.setForeground(QBrush(QColor(127, 0, 127), Qt.SolidPattern))
        boolean = QTextCharFormat()
        boolean.setForeground(QBrush(QColor(64, 112, 144), Qt.SolidPattern))
        self.highlightingRules = [highlightRule(QRegExp("\\b"+key+"\\b"), keyword) for key in
            ['from', 'import', 'for', 'if', 'else', 'elif']]
        self.highlightingRules.append(highlightRule(QRegExp("\\b[0-9]{1,10}\\b"), number))
        self.highlightingRules.append(highlightRule(QRegExp("\\b[0-9]{1,10}[.][0-9]{0,10}\\b"), number))
        self.highlightingRules.append(highlightRule(QRegExp("\\b[0-9]{1,10}([, ]*[0-9]{1,10}){1,10}"), number))
        self.highlightingRules.append(highlightRule(QRegExp("\'.*\'"), commit))
        self.highlightingRules.append(highlightRule(QRegExp("\".*\""), string))
        self.highlightingRules += [highlightRule(QRegExp("\\b"+key+"\\b"), boolean) for key in ['True', 'False']]
    
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
        self.setStyleSheet("font: 10pt \"Bitstream Vera Sans Mono\";")
        keywordSyntax(self)
    
class Script_Dialog(QDialog, Ui_Info_Dialog):
    def __init__(self, fileName, Point, Line, Chain, Shaft, Slider, Rod, Environment_variables, parent=None):
        super(Script_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.fileName = fileName
        self.Environment_variables = Environment_variables
        self.script = highlightTextEdit()
        self.verticalLayout.insertWidget(1, self.script)
        self.script.setPlainText(slvsProcessScript(Point, Line, Chain, Shaft, Slider, Rod))
    
    @pyqtSlot()
    def on_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.script.toPlainText())
        self.copy.setText(tr("Info_Dialog", "Copied!"))
    
    @pyqtSlot()
    def on_save_clicked(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save file...', self.Environment_variables+'/'+self.fileName+'.py', 'Python3 Script(*.py)')
        if fileName:
            if QFileInfo(fileName).suffix()!='py':
                fileName = fileName+'.py'
            with open(fileName, 'w', newline="") as f:
                f.write(self.script.toPlainText())
            print("Successful Saved: [{}]".format(fileName))
