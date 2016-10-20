# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_options import Ui_Dialog
from core.io.settings import Pyslvs_Settings_ini

class options_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(options_show, self).__init__(parent)
        self.setupUi(self)
        self.load_settings()
        #Connect
        self.Exit_button.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.Exit_button.button(QDialogButtonBox.Save).clicked.connect(self.apply)
        self.Exit_button.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.default)
    
    def load_settings(self):
        self.option_info = Pyslvs_Settings_ini()
        #General
        self.EnvVariable.setText(self.option_info.Environment_variables)
        self.ZoomFactor.setValue(self.option_info.Zoom_factor)
        self.TableToolLocation.setCurrentIndex(self.option_info.Table_tool_location)
        self.ViewBarLocation.setCurrentIndex(self.option_info.View_bar_location)
        self.ToolPanelLocation.setCurrentIndex(self.option_info.Tool_panel_location)
        self.OpenLastFile.setChecked(self.option_info.Open_last_file)
        #Appearance
        self.LinkingLinesColor.setCurrentIndex(self.option_info.Linking_lines_color)
        self.StayChainColor.setCurrentIndex(self.option_info.Stay_chain_color)
        self.AuxiliaryLineColor.setCurrentIndex(self.option_info.Auxiliary_line_color)
        self.AuxiliaryLimitLineColor.setCurrentIndex(self.option_info.Auxiliary_limit_line_color)
        self.TextColor.setCurrentIndex(self.option_info.Text_color)
    
    def default(self):
        """continue"""
    
    def apply(self):
        #General
        self.option_info.Environment_variables = self.EnvVariable.text()
        self.option_info.Zoom_factor = self.ZoomFactor.value()
        self.option_info.Table_tool_location = self.TableToolLocation.currentIndex()
        self.option_info.View_bar_location = self.ViewBarLocation.currentIndex()
        self.option_info.Tool_panel_location = self.ToolPanelLocation.currentIndex()
        self.option_info.Open_last_file = self.OpenLastFile.checked()
        #Appearance
        self.option_info.Linking_lines_color = self.LinkingLinesColor.currentIndex()
        self.option_info.Stay_chain_color = self.StayChainColor.currentIndex()
        self.option_info.Auxiliary_line_color = self.AuxiliaryLineColor.currentIndex()
        self.option_info.Auxiliary_limit_line_color = self.AuxiliaryLimitLineColor.currentIndex()
        self.option_info.Text_color = self.TextColor.currentIndex()
        #Save
        self.option_info.save()
    
    @pyqtSlot()
    def on_FileLocate_clicked(self):
        fileDir = QFileDialog.getExistingDirectory(self, 'Open Directory...', self.EnvVariable.text(), (QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        if fileDir: self.EnvVariable.setText(fileDir)
    
    @pyqtSlot(str)
    def on_EnvVariable_textEdited(self, path):
        if not os.path.isdir(path): self.EnvVariable.setText(self.option_info.Environment_variables)
