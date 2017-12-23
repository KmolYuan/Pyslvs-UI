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
from .info import VERSION, INFO, args
from .Ui_about import Ui_About_Dialog

#Turn simple string to html format.
html = lambda s: "<html><head/><body>{}</body></html>".format(s.replace('\n', '<br/>'))
title = lambda name, *s: '<h2>{}</h2>'.format(name)+('<h3>{}</h3>'.format('</h3><h3>'.join(s)) if s else '')
content = lambda *s: '<p>{}</p>'.format('</p><p>'.join(s))
orderList = lambda *s: '<ul><li>{}</li></ul>'.format('</li><li>'.join(s))

#Splash
class Pyslvs_Splash(QSplashScreen):
    def __init__(self, parent=None):
        super(Pyslvs_Splash, self).__init__(parent, QPixmap(":/icons/Splash.png"))
        self.showMessage("Version {}.{}.{}({})".format(*VERSION), (Qt.AlignBottom|Qt.AlignRight))

class Pyslvs_About(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(Pyslvs_About, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.Title.setText(html(title("Pyslvs")+content("Version {}.{}.{}({}) 2016-2017".format(*VERSION))))
        self.Content.setText(html(content(
            "Pyslvs is a Open Source support tools to help user solving 2D linkage problem.",
            "It can use in Mechanical Design and Simulation.",
            "This program using Python 3 with Python Solvespace.",
            "Pyslvs just like a ordinary CAD software, but use table to add and edit points.",
            "Within changing points location, finally give the answer to designer.",
            "We have these features:")+orderList(
            "2D Linkages dynamic simulation.",
            "Dimensional Synthesis of Planar Four-bar Linkages.",
            "Output points coordinate to Data Sheet (*.csv) format.",
            "Change canvas appearance.",
            "Draw dynamic simulation path with any point in the machinery.",
            "Using triangle iterate the mechanism results.")+content(
            "If you want to know about more, you can reference by our website."))
        )
        self.Versions.setText(html(orderList(*INFO)))
        self.Arguments.setText(html(content(
            "Startup arguments are as follows:")+orderList(
            "The loaded file when startup: {}".format(args.r),
            "Start Path: {}".format(args.i),
            "Enable solving warning: {}".format(args.w),
            "Fusion style: {}".format(args.fusion),
            "Debug mode: {}".format(args.debug_mode))+content(
            "Using the \"-h\" argument to view the help."))
        )
