# -*- coding: utf-8 -*-

"""About information."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from requests import get as get_url
from qtpy.QtCore import Qt, QCoreApplication
from qtpy.QtWidgets import QDialog, QWidget, QProgressDialog
from pyslvs_ui import __version__
from .info import SYS_INFO, ARGUMENTS
from .logging_handler import logger
from .about_ui import Ui_Dialog

LICENSE_STRING = (
    "This program is free software; "
    "you can redistribute it and/or modify it under the terms of the "
    "Affero General Public License (AGPL) as published by Affero, Inc. version 3. "
    "This program is distributed in the hope that it will be useful, "
    "but WITHOUT ANY WARRANTY; "
    "without even the implied warranty of "
    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."
)


def html(s: str) -> str:
    """Turn simple string to html format."""
    s = s.replace('\n', '<br/>')
    return f"<html><head/><body>{s}</body></html>"


def _title(name: str) -> str:
    """Wrap title."""
    return f'<h2>{name}</h2>'


def _content(*s: str) -> str:
    """Wrap as paragraph."""
    return f'<p>{"</p><p>".join(s)}</p>'


def _order_list(*s: str) -> str:
    """Wrap as list."""
    return f'<ul><li>{"</li><li>".join(s)}</li></ul>'


class PyslvsAbout(QDialog, Ui_Dialog):
    """Pyslvs about dialog."""

    def __init__(self, parent: QWidget):
        """About description strings."""
        super(PyslvsAbout, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.title_label.setText(html(_title("Pyslvs") + _content(
            f"Version {__version__} 2016-2021"
        )))
        self.description_text.setText(html(_content(
            "A GUI-based tool use to solving 2D linkage subject.",
            f"Author: {__author__}",
            f"Email: {__email__}",
            "If you want to know more, see to our website or contact the email.",
        )))
        self.license_text.setText(LICENSE_STRING)
        self.ver_text.setText(html(_order_list(*SYS_INFO)))
        self.args_text.setText(html(_content("Startup arguments are as follows:") + _order_list(
            f"Open with: {ARGUMENTS.filepath}",
            f"Start Path: {ARGUMENTS.c}",
            f"Fusion style: {ARGUMENTS.fusion}",
            f"Debug mode: {ARGUMENTS.debug_mode}",
            f"Specified kernel: {ARGUMENTS.kernel}",
        ) + _content("Use \"-h\" or \"--help\" argument to view the help.")))


def check_update(dlg: QProgressDialog) -> str:
    """Check for update."""
    ver_list = [int(v) for v in __version__.split('.') if v.isdigit()]
    logger.info(f"Getting update for \"{__version__}\":")
    m = len(ver_list)
    for i in range(m):
        if i == 0:
            text = "major"
        elif i == 1:
            text = "minor"
        else:
            text = "micro"
        dlg.setLabelText(f"Checking for {text}...")
        QCoreApplication.processEvents()
        if dlg.wasCanceled():
            return ""
        next_ver = ver_list[:m]
        next_ver[i] += 1
        for j in range(i + 1, m):
            next_ver[j] = 0
        if i == 0:
            next_ver[1] = 1
        elif i == 1:
            if next_ver[1] > 12:
                dlg.setValue(i + 1)
                continue
        url = (
            f"https://github.com/KmolYuan/Pyslvs-UI/releases/tag/"
            f"v{next_ver[0]}.{next_ver[1]:02}.{next_ver[2]}"
        )
        request = get_url(url)
        dlg.setValue(i + 1)
        if request.status_code == 200:
            dlg.setValue(m)
            return url
    return ""
