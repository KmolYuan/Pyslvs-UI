# -*- coding: utf-8 -*-

"""Python script output function."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, Tuple, List, Sequence, Set, Optional
from qrcode import make
from qrcode.image.base import BaseImage
from numpy import full, ndarray, uint8
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QTextEdit,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QSizePolicy,
)
from qtpy.QtGui import QIcon, QPixmap, QImage, QWheelEvent, QFont
from .script_ui import Ui_Dialog

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase

_Expr = Sequence[Tuple[str, ...]]
_SCRIPT = """
from pyslvs import parse_vpoints, t_config, expr_solving

if __name__ == '__main__':
    vpoints = parse_vpoints(
        "M["\n{}
        "]")
    exprs = t_config(vpoints, {})
    mapping = {{n: f'P{{n}}' for n in range(len(vpoints))}}
    pos = expr_solving(exprs, vpoints, {})
    print(data_dict)
    print(pos)
"""
_CAL_SCRIPT = """
from pyslvs import {}

# {} are known

if __name__ == '__main__':
"""


class _NpImage(BaseImage):
    """NumPy image for QR code."""

    def __init__(self, border, width, box_size, *args, **kwargs):
        super(_NpImage, self).__init__(border, width, box_size, *args, **kwargs)

    def new_image(self, **kwargs) -> ndarray:
        """Build the image class."""
        return full((self.pixel_size, self.pixel_size, 3), 255, dtype=uint8)

    def drawrect(self, row: int, col: int) -> None:
        """Draw a single rectangle of the QR code."""
        (x, y), (x2, y2) = self.pixel_box(row, col)
        for r in range(self.box_size):
            self._img[y + r, x:x2 + 1] = (0, 0, 0)

    def get_qimage(self) -> QImage:
        """To QImage."""
        height, width, color = self._img.shape
        return QImage(
            self._img.data,
            width,
            height,
            color * height,
            QImage.Format_RGB888
        )

    def save(self, stream, kind=None) -> None:
        """Do nothing."""
        pass


def slvs_process_script(
    script: Sequence[str],
    inputs: Sequence[Tuple[int, int]]
) -> str:
    """Return parser function script."""
    return _SCRIPT.format(
        '\n'.join(" " * 8 + f'"{expr}, "' for expr in script),
        inputs,
        {pair: 0. for pair in inputs}
    )


def _expr_to_script(exprs: _Expr) -> str:
    cmd = []
    functions = set()
    symbols: Set[str] = set()
    targets = set()
    for expr in exprs:
        func = expr[0].lower()
        target = expr[-1].lower()
        sym = tuple(e.lower() for e in expr[1:-1])
        args = ", ".join(sym)
        cmd.append(" " * 4 + f"{target} = {func}({args})")
        functions.add(func)
        symbols.update(sym)
        targets.add(target)
    script = _CAL_SCRIPT.format(", ".join(sorted(functions)),
                                ", ".join(sorted(symbols - targets)))
    return script + '\n'.join(cmd)


class _ScriptBrowser(QTextEdit):
    """Custom text browser to implement text zooming."""

    def __init__(self, parent: QWidget):
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
    image: QPixmap

    def __init__(
        self,
        icon: QIcon,
        script: str,
        filename: str,
        file_format: List[str],
        parent: MainWindowBase,
        *,
        compressed_script: str = "M[]",
        exprs: Optional[_Expr] = None
    ):
        """Input parameters:

        + Script
        + Lexer
        + File name
        + File suffix
        """
        super(ScriptDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint
                            & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(icon)
        self.btn_box.button(QDialogButtonBox.Close).setDefault(True)
        # Calculation function
        if exprs is not None:
            script += "\n###\n" + _expr_to_script(exprs)
        self.script_view = _ScriptBrowser(self)
        self.script_view.setText(script)
        self.main_layout.insertWidget(0, self.script_view)
        self.filename = filename
        self.file_format = file_format
        self.output_to = parent.output_to
        self.save_reply_box = parent.save_reply_box
        self.setWindowTitle(self.filename)
        self.btn_box.button(QDialogButtonBox.Save).clicked.connect(
            self.__save)

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
        image = make(self.compressed_script, image_factory=_NpImage)
        self.image = QPixmap.fromImage(image.get_qimage())

    def __save(self) -> None:
        """Save to specific format."""
        path = self.output_to("Script", self.file_format)
        if not path:
            return
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(self.script_view.toPlainText())
        self.save_reply_box("Script", path)

    @Slot(name='on_copy_btn_clicked')
    def __copy(self) -> None:
        """Copy to clipboard."""
        QApplication.clipboard().setText(
            self.compressed_script if self.compressed_script else
            self.script_view.toPlainText()
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
