# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from pygments.lexers import Python3Lexer
from typing import (
    Tuple,
    List,
    Dict,
    Callable,
    Iterator,
    Union,
)
from core.QtModules import (
    Qt,
    QApplication,
    QWidget,
    QMessageBox,
    QDesktopServices,
    QUrl,
    QInputDialog,
    QFileInfo,
    QFileDialog,
    QProgressDialog,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QCheckBox,
)
from core.info import (
    PyslvsAbout,
    check_update,
    __version__,
)
from core.io import (
    ScriptDialog,
    slvsProcessScript,
    AddTable,
    EditPointTable,
    SlvsParser,
    slvs_output,
    dxfSketch,
    QTIMAGES,
    strbetween,
)
from core.libs import parse_params, PMKSLexer


def _openURL(url: str):
    """Use to open link."""
    QDesktopServices.openUrl(QUrl(url))


def _v_to_slvs(self) -> Callable[[], Tuple[Tuple[int, int]]]:
    """Solvespace edges."""
    
    def v_to_slvs() -> Iterator[Tuple[int, int]]:
        for vlink in self.EntitiesLink.data():
            if vlink.name == 'ground':
                continue
            for i, p in enumerate(vlink.points):
                if i == 0:
                    continue
                yield (vlink.points[0], p)
                if i > 1:
                    yield (vlink.points[i-1], p)
    
    return v_to_slvs


def _readSlvs(self, file_name: str):
    """Read slvs format.
    
    + Choose a layout.
    + Read the entities of the layout.
    """
    parser = SlvsParser(file_name)
    if not parser.isValid():
        QMessageBox.warning(self,
            "Format error",
            "The format is not support."
        )
        return
    layout, ok = QInputDialog.getItem(self,
        "Solvespace layout",
        "Choose a layout:\n" +
        "(Please know that the layout must contain a sketch only.)",
        parser.layouts(),
        0,
        False
    )
    if not ok:
        parser.close()
        return
    self.clear()
    self.FileWidget.reset()
    print("Read from layout: {}".format(layout))
    expr = parser.parse(layout)
    parser.close()
    self.parseExpression(expr)


def _settings(self) -> Tuple[Tuple[QWidget, Union[int, float, bool]]]:
    """Give the settings of all option widgets."""
    return (
        (self.linewidth_option, 3),
        (self.fontsize_option, 15),
        (self.pathwidth_option, 3),
        (self.scalefactor_option, 10),
        (self.selectionradius_option, 10),
        (self.linktrans_option, 0),
        (self.marginfactor_option, 5),
        (self.jointsize_option, 5),
        (self.zoomby_option, 0),
        (self.snap_option, 1.),
        (self.undolimit_option, 32),
        (self.planarsolver_option, 0),
        (self.titlefullpath_option, False),
        (self.consoleerror_option, False),
        #Do not save settings.
        (self.dontsave_option, True),
    )


def dragEnterEvent(self, event):
    """Drag file in to our window."""
    mimeData = event.mimeData()
    if not mimeData.hasUrls():
        return
    for url in mimeData.urls():
        file_name = url.toLocalFile()
        if QFileInfo(file_name).suffix() in ('pyslvs', 'slvs'):
            event.acceptProposedAction()


def dropEvent(self, event):
    """Drop file in to our window."""
    file_name = event.mimeData().urls()[-1].toLocalFile()
    suffix = QFileInfo(file_name).suffix()
    if suffix == 'pyslvs':
        self.FileWidget.read(file_name)
    elif suffix == 'slvs':
        _readSlvs(self, file_name)
    event.acceptProposedAction()


def workbookNoSave(self):
    """Workbook not saved signal."""
    self.FileWidget.changed = True
    not_yet_saved = " (not yet saved)"
    self.setWindowTitle(
        self.windowTitle().replace(not_yet_saved, '') +
        not_yet_saved
    )


def workbookSaved(self):
    """Workbook saved signal."""
    self.FileWidget.changed = False
    self.on_windowTitle_fullpath_clicked()


def on_windowTitle_fullpath_clicked(self):
    """Set the option 'window title will show the fullpath'."""
    file_name = self.FileWidget.file_name
    self.setWindowTitle("Pyslvs - {}".format(
        file_name.absoluteFilePath()
        if self.titlefullpath_option.isChecked()
        else file_name.fileName()
    ) + (" (not yet saved)" if self.FileWidget.changed else ''))


def on_action_Get_Help_triggered(self):
    """Open website: mde.tw"""
    _openURL("http://mde.tw")


def on_action_Pyslvs_com_triggered(self):
    """Open website: pyslvs.com"""
    _openURL("http://www.pyslvs.com/blog/index.html")


def on_action_github_repository_triggered(self):
    """Open website: Github repository."""
    _openURL("https://github.com/KmolYuan/Pyslvs-PyQt5")


def on_action_About_Pyslvs_triggered(self):
    """Open Pyslvs about."""
    dlg = PyslvsAbout(self)
    dlg.show()
    dlg.exec_()


def on_action_Console_triggered(self):
    """Open GUI console."""
    self.OptionTab.setCurrentIndex(2)
    self.History_tab.setCurrentIndex(1)


def on_action_Example_triggered(self):
    """Load examples from 'FileWidget'.
    Return true if successed.
    """
    if self.FileWidget.loadExample():
        self.on_action_See_Expression_triggered()
        self.MainCanvas.zoomToFit()


def on_action_Import_Example_triggered(self):
    """Import a example and merge it to canvas."""
    self.FileWidget.loadExample(isImport = True)


def on_action_New_Workbook_triggered(self):
    """Create (Clean) a new workbook."""
    if self.checkFileChanged():
        return
    self.clear()
    self.FileWidget.reset()
    print("Created a new workbook.")


def clear(self):
    """Clear to create commit stage."""
    self.mechanism_storage_name_tag.clear()
    self.mechanism_storage.clear()
    self.CollectionTabPage.clear()
    self.NumberAndTypeSynthesis.clear()
    self.InputsWidget.clear()
    self.DimensionalSynthesis.clear()
    self.EntitiesPoint.clear()
    self.EntitiesLink.clear()
    self.Entities_Expr.clear()
    self.resolve()


def on_action_Import_PMKS_server_triggered(self):
    """Load PMKS URL and turn it to expression."""
    URL, ok = QInputDialog.getText(self,
        "PMKS URL input",
        "Please input link string:"
    )
    if not ok:
        return
    if not URL:
        QMessageBox.warning(self,
            "Loading failed",
            "Your link is in an incorrect format."
        )
        return
    try:
        for s in URL.split('?')[-1].split('&'):
            if 'mech=' in s:
                expr = s.replace('mech=', '').split('|')
                break
        textList = [s for s in expr if s not in ('', " ", '\n')]
        expression = []
        while textList:
            item = textList.pop(0).split(',')[:-1]
            for i, e in enumerate(reversed(item)):
                if e in ['R', 'P', 'RP']:
                    t = -(i+1)
                    break
            links = item[:t]
            item = item[t:]
            expression.append("J[{}, P[{}], L[{}]]".format(
                "{}:{}".format(item[0], item[-1]) if item[0]!='R' else 'R',
                ", ".join((item[1], item[2])),
                ", ".join(links)
            ))
        expression = "M[{}]".format(", ".join(expression))
    except:
        QMessageBox.warning(self,
            "Loading failed",
            "Your link is in an incorrect format."
        )
    else:
        self.parseExpression(expression)


def parseExpression(self, expr: str):
    """Parse expression."""
    try:
        args_list = parse_params(expr)
    except Exception as e:
        QMessageBox.warning(self,
            "Loading failed",
            "Your expression is in an incorrect format.\n" + str(e)
        )
    else:
        for args in args_list:
            linkNames = tuple(
                vlink.name for vlink in self.EntitiesLink.data()
            )
            links = args[0].split(',')
            for linkName in links:
                #If link name not exist.
                if linkName not in linkNames:
                    self.addLink(linkName, 'Blue')
            rowCount = self.EntitiesPoint.rowCount()
            self.CommandStack.beginMacro("Add {{Point{}}}".format(rowCount))
            self.CommandStack.push(AddTable(self.EntitiesPoint))
            self.CommandStack.push(EditPointTable(
                rowCount,
                self.EntitiesPoint,
                self.EntitiesLink,
                args
            ))
            self.CommandStack.endMacro()


def addEmptyLinkGroup(self, linkcolor: Dict[str, str]):
    """Use to add empty link when loading database."""
    for name, color in linkcolor.items():
        if name != 'ground':
            self.addLink(name, color)


def on_action_Load_File_triggered(self):
    """Load workbook."""
    if self.checkFileChanged():
        return
    file_name = self.inputFrom(
        "Workbook database",
        ["Pyslvs workbook (*.pyslvs)",
        "Solvespace module (*.slvs)"]
    )
    if not file_name:
        return
    suffix = QFileInfo(file_name).suffix()
    if suffix == 'pyslvs':
        self.FileWidget.read(file_name)
    elif suffix == 'slvs':
        _readSlvs(self, file_name)
    self.MainCanvas.zoomToFit()


def on_action_Import_Workbook_triggered(self):
    """Import from workbook."""
    if self.checkFileChanged():
        return
    file_name = self.inputFrom(
        "Workbook database (Import)",
        ["Pyslvs workbook (*.pyslvs)"]
    )
    if not file_name:
        return
    self.FileWidget.importMechanism(file_name)


def on_action_Save_triggered(self, isBranch: bool):
    """Save action."""
    file_name = self.FileWidget.file_name.absoluteFilePath()
    if self.FileWidget.file_name.suffix()=='pyslvs':
        self.FileWidget.save(file_name, isBranch)
    else:
        self.on_action_Save_as_triggered(isBranch)


def on_action_Save_as_triggered(self, isBranch: bool):
    """Save as action."""
    file_name = self.outputTo("workbook", ["Pyslvs workbook (*.pyslvs)"])
    if file_name:
        self.FileWidget.save(file_name, isBranch)
        self.saveReplyBox("Workbook", file_name)


def on_action_Save_branch_triggered(self):
    """Save as new branch action."""
    self.on_action_Save_triggered(True)


def on_action_Output_to_Solvespace_triggered(self):
    """Solvespace 2d save function."""
    file_name = self.outputTo(
        "Solvespace sketch",
        ["Solvespace module (*.slvs)"]
    )
    if not file_name:
        return
    slvs_output(
        self.EntitiesPoint.dataTuple(),
        _v_to_slvs(self),
        file_name
    )
    self.saveReplyBox("Solvespace sketch", file_name)


def on_action_Output_to_DXF_triggered(self):
    """DXF 2d save function."""
    file_name = self.outputTo(
        "Drawing Exchange Format",
        ["Drawing Exchange Format (*.dxf)"]
    )
    if not file_name:
        return
    dxfSketch(
        self.EntitiesPoint.dataTuple(),
        _v_to_slvs(self),
        file_name
    )
    self.saveReplyBox("Drawing Exchange Format", file_name)


def on_action_Output_to_Picture_triggered(self):
    """Picture save function."""
    file_name = self.outputTo("picture", QTIMAGES)
    if not file_name:
        return
    pixmap = self.MainCanvas.grab()
    pixmap.save(file_name, format=QFileInfo(file_name).suffix())
    self.saveReplyBox("Picture", file_name)


def outputTo(self, formatName: str, formatChoose: List[str]) -> str:
    """Simple to support mutiple format."""
    suffix0 = strbetween(formatChoose[0], '(', ')').split('*')[-1]
    file_name, suffix = QFileDialog.getSaveFileName(
        self,
        "Save to {}...".format(formatName),
        self.env+'/'+self.FileWidget.file_name.baseName()+suffix0,
        ';;'.join(formatChoose)
    )
    if file_name:
        suffix = strbetween(suffix, '(', ')').split('*')[-1]
        print("Format: {}".format(suffix))
        if QFileInfo(file_name).suffix()!=suffix[1:]:
            file_name += suffix
        self.setLocate(QFileInfo(file_name).absolutePath())
    return file_name


def saveReplyBox(self, title: str, file_name: str):
    """Show message when successfully saved."""
    size = QFileInfo(file_name).size()
    print("Size: {}".format(
        "{} MB".format(round(size/1024/1024, 2))
        if size/1024//1024 else "{} KB".format(round(size/1024, 2))
    ))
    QMessageBox.information(self,
        title,
        "Successfully converted:\n{}".format(file_name)
    )
    print("Successful saved: [\"{}\"]".format(file_name))


def inputFrom(self,
    formatName: str,
    formatChoose: List[str],
    multiple: bool = False
) -> str:
    """Get file name(s)."""
    args = (
        "Open {} file{}...".format(formatName, 's' if multiple else ''),
        self.env,
        ';;'.join(formatChoose)
    )
    if multiple:
        file_name_s, suffix = QFileDialog.getOpenFileNames(self, *args)
    else:
        file_name_s, suffix = QFileDialog.getOpenFileName(self, *args)
    if file_name_s:
        suffix = strbetween(suffix, '(', ')').split('*')[-1]
        print("Format: {}".format(suffix))
        if type(file_name_s) == str:
            self.setLocate(QFileInfo(file_name_s).absolutePath())
        else:
            self.setLocate(QFileInfo(file_name_s[0]).absolutePath())
    return file_name_s


def on_action_Output_to_PMKS_triggered(self):
    """Output to PMKS as URL."""
    url = "http://designengrlab.github.io/PMKS/pmks.html?mech="
    urlTable = []
    for row in range(self.EntitiesPoint.rowCount()):
        TypeAndAngle = self.EntitiesPoint.item(row, 2).text().split(':')
        pointData = [
            self.EntitiesPoint.item(row, 1).text(),
            TypeAndAngle[0],
            self.EntitiesPoint.item(row, 4).text(),
            self.EntitiesPoint.item(row, 5).text(),
        ]
        if len(TypeAndAngle)==2:
            pointData.append(TypeAndAngle[1])
        pointData.append('tfff')
        urlTable.append(','.join(pointData))
    url += '|'.join(urlTable)+'|'
    text = '\n'.join([
        "Copy and past this link to web browser:\n",
        url + '\n',
        "If you have installed Microsoft Silverlight in " +
        "Internet Explorer as default browser, " +
        "just click \"Open\" button to open it in PMKS website."
    ])
    reply = QMessageBox.information(self,
        "PMKS web server",
        text,
        (QMessageBox.Save | QMessageBox.Open | QMessageBox.Close),
        QMessageBox.Save
    )
    if reply == QMessageBox.Open:
        _openURL(url)
    elif reply == QMessageBox.Save:
        QApplication.clipboard().setText(url)


def on_action_Output_to_Picture_clipboard_triggered(self):
    """Capture the canvas image to clipboard."""
    QApplication.clipboard().setPixmap(self.MainCanvas.grab())
    QMessageBox.information(self,
        "Captured!",
        "Canvas widget picture is copy to clipboard."
    )


def on_action_See_Expression_triggered(self):
    """Output as expression."""
    context = ",\n".join(" " * 4 + vpoint.expr for vpoint in self.EntitiesPoint.data())
    dlg = ScriptDialog(
        "#Generate by Pyslvs v{}.{}.{} ({})\n".format(*__version__) +
        ("M[\n{}\n]".format(context) if context else "M[]"),
        PMKSLexer(),
        "Pyslvs expression",
        ["Text file (*.txt)"],
        self
    )
    dlg.show()
    dlg.exec_()


def on_action_See_Python_Scripts_triggered(self):
    """Output to Python script for Jupyter notebook."""
    dlg = ScriptDialog(
        "#Generate by Pyslvs v{}.{}.{} ({})\n".format(*__version__) +
        slvsProcessScript(self.EntitiesPoint.data(), self.EntitiesLink.data()),
        Python3Lexer(),
        "Python script",
        ["Python3 Script (*.py)"],
        self
    )
    dlg.show()
    dlg.exec_()


def on_action_Check_update_triggered(self):
    """Check for update."""
    progdlg = QProgressDialog("Checking update ...", "Cancel", 0, 3, self)
    progdlg.setAttribute(Qt.WA_DeleteOnClose, True)
    progdlg.setWindowTitle("Check for update")
    progdlg.resize(400, progdlg.height())
    progdlg.setModal(True)
    progdlg.show()
    url = check_update(progdlg)
    if not url:
        QMessageBox.information(self,
            "Pyslvs is up to date",
            "You are using the latest version of Pyslvs."
        )
        return
    reply = QMessageBox.question(
        self,
        "Pyslvs has update",
        "Do you want to get it from Github?",
        (QMessageBox.Ok | QMessageBox.Cancel),
        QMessageBox.Ok
    )
    if reply == QMessageBox.Ok:
        _openURL(url)


def checkFileChanged(self) -> bool:
    """If the user has not saved the change.
    
    Return True if user want to "discard" the operation.
    """
    if not self.FileWidget.changed:
        return False
    reply = QMessageBox.question(
        self,
        "Message",
        "Are you sure to quit?\nAny changes won't be saved.",
        (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel),
        QMessageBox.Save
    )
    if reply == QMessageBox.Save:
        self.on_action_Save_triggered()
        return self.FileWidget.changed
    elif reply == QMessageBox.Discard:
        return False
    return True


def restoreSettings(self):
    """Restore Pyslvs settings."""
    for option in _settings(self):
        widget = option[0]
        name = widget.objectName()
        if type(widget) in (QSpinBox, QDoubleSpinBox):
            widget.setValue(
                self.settings.value(name, option[-1], type=type(option[-1]))
            )
        elif type(widget) == QComboBox:
            widget.setCurrentIndex(
                self.settings.value(name, option[-1], type=int)
            )
        elif type(widget) == QCheckBox:
            widget.setChecked(
                self.settings.value(name, option[-1], type=bool)
            )


def saveSettings(self):
    """Save Pyslvs settings (auto save when close event)."""
    if self.dontsave_option.isChecked():
        self.settings.clear()
        return
    for option in _settings(self):
        widget = option[0]
        name = widget.objectName()
        if type(widget) in (QSpinBox, QDoubleSpinBox):
            self.settings.setValue(name, widget.value())
        elif type(widget) == QComboBox:
            self.settings.setValue(name, widget.currentIndex())
        elif type(widget) == QCheckBox:
            self.settings.setValue(name, widget.isChecked())


def resetOptions(self):
    """Reset options with default value."""
    for option in _settings(self):
        widget = option[0]
        if type(widget) in (QSpinBox, QDoubleSpinBox):
            widget.setValue(option[-1])
        elif type(widget) == QComboBox:
            widget.setCurrentIndex(option[-1])
        elif type(widget) == QCheckBox:
            widget.setChecked(option[-1])

def readFromArgs(self):
    if not self.args.r:
        return
    suffix = QFileInfo(self.args.r).suffix()
    if suffix == 'pyslvs':
        self.FileWidget.read(self.args.r)
    elif suffix == 'slvs':
        _readSlvs(self, self.args.r)
    else:
        print("Unsupported format has been ignore when startup.")
