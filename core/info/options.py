# -*- coding: utf-8 -*-
#import os.path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_options import Ui_Dialog
from core.io.settings import Pyslvs_Settings_ini

class options_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(options_show, self).__init__(parent)
        self.setupUi(self)
        self.option_info = Pyslvs_Settings_ini()
        self.EnvVariable.setText(self.option_info.Environment_variables)
        self.ZoomFactor.setValue(self.option_info.Zoom_factor)
        self.TableToolLocation.setCurrentIndex(self.option_info.Table_tool_location)
        self.ViewBarLocation.setCurrentIndex(self.option_info.View_bar_location)
        self.ToolPanelLocation.setCurrentIndex(self.option_info.Tool_panel_location)
