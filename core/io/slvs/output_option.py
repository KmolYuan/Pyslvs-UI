# -*- coding: utf-8 -*-

"""Output dialog for slvs format."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Callable
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
)
from core.libs import VPoint
from .frame import slvs_frame
from .part import slvs_part
from .Ui_output_option import Ui_Dialog


class SlvsOutputDialog(QDialog, Ui_Dialog):
    
    """Setting the path and output name."""
    
    def __init__(self,
        env: str,
        file_name: str,
        vpoints: Tuple[VPoint],
        v_to_slvs: Callable[[], Tuple[int, int]],
        parent
    ):
        """Comes in environment variable, workbook name
            and parameters of 'v_to_slvs' function.
        """
        super(SlvsOutputDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.path_edit.setPlaceholderText(env)
        self.filename_edit.setPlaceholderText(file_name)
        self.vpoints = vpoints
        self.v_to_slvs = v_to_slvs
    
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
        """Write file and close if saved successfully.
        
        Output types:
        + Assembly
        + Only wire frame
        """
        
        def getname(widget: QTextEdit, *, ispath: bool = False) -> str:
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
        
        dir = QDir(getname(self.path_edit, ispath=True))
        if self.newfolder_option.isChecked():
            new_folder = self.filename_edit.placeholderText()
            if (not dir.mkdir(new_folder)) and self.warn_radio.isChecked():
                QMessageBox.warning(
                    self,
                    "Folder exist",
                    "The folder named {} is exist.".format(new_folder)
                )
                return
            dir.cd(new_folder)
            del new_folder
        file_name = dir.filePath(getname(self.filename_edit) + '.slvs')
        if self.warn_radio.isChecked() and isfile(file_name):
            QMessageBox.warning(
                self,
                "File exist",
                "The file {} is exist.".format(file_name)
            )
            return
        
        #Wire frame
        slvs_frame(self.vpoints, self.v_to_slvs, file_name)
        
        #Open Solvespace from commend line if available.
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
            if self.warn_radio.isChecked() and isfile(file_name):
                QMessageBox.warning(
                    self,
                    "File exist",
                    "The file {} is exist.".format(file_name)
                )
                return
            slvs_part(
                [self.vpoints[i] for i in points],
                self.link_radius.value(),
                file_name
            )
        
        self.accept()
