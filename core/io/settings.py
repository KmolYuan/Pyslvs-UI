from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Pyslvs_Settings_ini():
    def __init__(self):
        self.settings = QSettings("./Pyslvs_Settings.ini", QSettings.IniFormat)
        #General
        self.Environment_variables = self.settings.value("Environment_variables", "../")
        self.Zoom_factor = int(self.settings.value("Zoom_factor", 200))
        self.Table_tool_location = int(self.settings.value("Table_tool_location", 0))
        self.View_bar_location = int(self.settings.value("View_bar_location", 0))
        self.Tool_panel_location = int(self.settings.value("Tool_panel_location", 0))
        self.Open_last_file = bool(self.settings.value("Open_last_file", False))
        #Appearance
        self.Linking_lines_color = int(self.settings.value("Linking_lines_color", 0))
        self.Stay_chain_color = int(self.settings.value("Stay_chain_color", 0))
        self.Auxiliary_line_color = int(self.settings.value("Auxiliary_line_color", 0))
        self.Auxiliary_limit_line_color = int(self.settings.value("Auxiliary_limit_line_color", 0))
        self.Text_color = int(self.settings.value("Text_color", 0))
    
    def save(self):
        #General
        self.settings.setValue("Environment_variables", QVariant(self.Environment_variables))
        self.settings.setValue("Zoom_factor", QVariant(self.Zoom_factor))
        self.settings.setValue("Table_tool_location", QVariant(self.Table_tool_location))
        self.settings.setValue("View_bar_location", QVariant(self.View_bar_location))
        self.settings.setValue("Tool_panel_location", QVariant(self.Tool_panel_location))
        self.settings.setValue("Open_last_file", QVariant(self.Open_last_file))
        #Appearance
        self.settings.setValue("Linking_lines_color", QVariant(self.Linking_lines_color))
        self.settings.setValue("Stay_chain_color", QVariant(self.Stay_chain_color))
        self.settings.setValue("Auxiliary_line_color", QVariant(self.Auxiliary_line_color))
        self.settings.setValue("Auxiliary_limit_line_color", QVariant(self.Auxiliary_limit_line_color))
        self.settings.setValue("Text_color", QVariant(self.Text_color))
        print("Saved Settings.")
