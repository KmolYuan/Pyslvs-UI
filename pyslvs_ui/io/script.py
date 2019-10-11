# -*- coding: utf-8 -*-

"""Python script output function."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, Tuple, List, Sequence
import qrcode
from PIL.ImageQt import ImageQt
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import (
    QApplication,
    QDialog,
    QTextEdit,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QSizePolicy,
)
from qtpy.QtGui import QIcon, QPixmap, QWheelEvent, QFont
from .script_ui import Ui_Dialog
if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase


_SCRIPT = """
from pyslvs import (
    parse_vpoints,
    vpoints_configure,
    data_collecting,
    expr_solving,
)

if __name__ == '__main__':
    vpoints = parse_vpoints(
        "M["\n{0}
        "]")
    exprs = vpoints_configure(vpoints, {1})
    mapping = {{n: f'P{{n}}' for n in range(len(vpoints))}}
    data_dict, dof = data_collecting(exprs, mapping, vpoints)
    pos = expr_solving(exprs, mapping, vpoints, [0.])
    print(data_dict)
    print(f"DOF:{{dof}}")
    print(pos)
"""


def slvs_process_script(
    script: Sequence[str],
    inputs: Sequence[Tuple[int, int]]
) -> str:
    """Return parser function script."""
    return _SCRIPT.format(
        '\n'.join(" " * 8 + f'"{expr}, "' for expr in script),
        inputs
    )


class _ScriptBrowser(QTextEdit):

    """Custom text browser to implement text zooming."""

    def __init__(self, parent: QWidget) -> None:
        super(_ScriptBrowser, self).__init__(parent)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setFont(QFont("Consolas"))
        self.setReadOnly(True)
        self.zoomIn(3)

    def wheelEvent(self, event: QWheelEvent) -> None:
        super(_ScriptBrowser, self).wheelEvent(event)
        if QApplication.keyboardModifiers() != Qt.ControlModifier:
            return
        if event.angleDelta().y() > 0:
            self.zoomIn(1)
        else:
            self.zoomOut(1)


class ScriptDialog(QDialog, Ui_Dialog):

    """Dialog of script preview."""

    def __init__(
        self,
        icon: QIcon,
        script: str,
        filename: str,
        file_format: List[str],
        parent: MainWindowBase,
        *,
        compressed_script: str = "M[]"
    ):
        """Input parameters:

        + Script
        + Lexer
        + File name
        + File suffix
        """
        super(ScriptDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
            self.windowFlags()
            & ~Qt.WindowContextHelpButtonHint
            | Qt.WindowMaximizeButtonHint
        )
        self.setWindowIcon(icon)
        self.script_view = _ScriptBrowser(self)
        self.script_view.setText(script)
        self.main_layout.insertWidget(0, self.script_view)
        self.filename = filename
        self.file_format = file_format
        self.output_to = parent.output_to
        self.save_reply_box = parent.save_reply_box
        self.setWindowTitle(self.filename)

        # Compressed script
        self.compressed_script = compressed_script
        if self.compressed_script == "M[]":
            self.show_qrcode.setVisible(False)
            return
        line_edit = QLineEdit(self)
        line_edit.setText(self.compressed_script)
        line_edit.setReadOnly(True)
        self.main_layout.insertWidget(1, line_edit)
        # Image display
        image = qrcode.make(self.compressed_script)
        self.image: QPixmap = QPixmap.fromImage(ImageQt(image.resize((500, 500))))

    @Slot(name='on_copy_clicked')
    def __copy(self) -> None:
        """Copy to clipboard."""
        QApplication.clipboard().setText(
            self.compressed_script if self.compressed_script else self.script_view.toPlainText()
        )

    @Slot(name='on_show_qrcode_clicked')
    def __show_qrcode(self) -> None:
        """Save to image file."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Mechanism QR code")
        dlg.setModal(True)
        layout = QVBoxLayout(dlg)
        label = QLabel(dlg)
        layout.addWidget(label)
        label.setPixmap(self.image)
        dlg.setFixedSize(self.image.size())
        dlg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        dlg.show()
