# -*- coding: utf-8 -*-

"""Output dialog for slvs format."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Callable, Optional
from os.path import isdir, isfile
import shutil
from subprocess import Popen, DEVNULL
from core.QtModules import (
    pyqtSlot,
    Qt,
    QDialog,
    QDir,
    QMessageBox,
    QFileDialog,
    QTextEdit,
    QWidget,
)
from core.libs import VPoint
from .slvs import slvs_frame, slvs_part
from .Ui_output_option import Ui_Dialog


def _getname(widget: QTextEdit, *, ispath: bool = False) -> str:
    """Return the file name of widget."""
    text = widget.text()
    if ispath:
        if isdir(text):
            return text
        else:
            return widget.placeholderText()
    if text:
        return "".join(x for x in text if x.isalnum() or (x in "._- "))
    else:
        return widget.placeholderText()


class _OutputDialog(QDialog, Ui_Dialog):
    
    """Output dialog template."""
    
    def __init__(self, env: str, file_name: str, format: str, parent: QWidget):
        """Comes in environment variable and workbook name."""
        super(_OutputDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.path_edit.setPlaceholderText(env)
        self.filename_edit.setPlaceholderText(file_name)
        self.setWindowTitle("Export {} project".format(format))
    
    @pyqtSlot()
    def on_choosedir_button_clicked(self):
        """Choose path and it will be set as environment variable if accepted."""
        path = self.path_edit.text()
        if not isdir(path):
            path = self.path_edit.placeholderText()
        path = QFileDialog.getExistingDirectory(self, "Choose a directory", path)
        if path:
            self.path_edit.setText(path)
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """Do the saving work, return True if done."""
        if self.do():
            self.accept()
    
    def exist_warning(self, name: str, *, folder: bool = False):
        """Show the "file is exist" message box."""
        if self.warn_radio.isChecked():
            QMessageBox.warning(self,
                "{} exist".format("Folder" if folder else "File"),
                "The folder named {} is exist.".format(name) if folder else
                "The file {} is exist.".format(name)
            )
    
    def do(self) -> Optional[bool]:
        """Do the saving work here."""
        raise NotImplementedError("virtual function")


class SlvsOutputDialog(_OutputDialog):
    
    """Setting the path and output name."""
    
    def __init__(self,
        env: str,
        file_name: str,
        vpoints: Tuple[VPoint],
        v_to_slvs: Callable[[], Tuple[int, int]],
        parent: QWidget
    ):
        """Parameters of 'v_to_slvs' function."""
        super(SlvsOutputDialog, self).__init__(env, file_name, "Solvespace module", parent)
        self.vpoints = vpoints
        self.v_to_slvs = v_to_slvs
    
    def do(self):
        """Write file and close if saved successfully.
        
        Output types:
        + Assembly
        + Only wire frame
        """
        dir = QDir(_getname(self.path_edit, ispath=True))
        if self.newfolder_option.isChecked():
            new_folder = self.filename_edit.placeholderText()
            if (not dir.mkdir(new_folder)):
                self.exist_warning(new_folder, folder=True)
                return
            dir.cd(new_folder)
            del new_folder
        file_name = dir.filePath(_getname(self.filename_edit) + '.slvs')
        if isfile(file_name):
            self.exist_warning(file_name)
            return
        
        #Wire frame
        slvs_frame(self.vpoints, self.v_to_slvs, file_name)
        
        #Open Solvespace by commend line if available.
        cmd = shutil.which("solvespace")
        if cmd:
            Popen([cmd , file_name], stdout=DEVNULL, stderr=DEVNULL)
        
        if self.frame_radio.isChecked():
            self.accept()
            return
        
        #Assembly
        vlinks = {}
        for i, vpoint in enumerate(self.vpoints):
            for link in vpoint.links:
                if link in vlinks:
                    vlinks[link].add(i)
                else:
                    vlinks[link] = {i}
        for name, points in vlinks.items():
            if name == 'ground':
                continue
            file_name = dir.filePath(name + '.slvs')
            if isfile(file_name):
                self.exist_warning(file_name)
                return
            slvs_part([
                self.vpoints[i] for i in points
            ], self.link_radius.value(), file_name)
        
        return True
