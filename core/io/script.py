# -*- coding: utf-8 -*-

"""Python script output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, List
from pygments import highlight
from pygments.lexer import RegexLexerMeta
from pygments.formatters import HtmlFormatter
from pygments.styles import (
    get_style_by_name,
    get_all_styles,
)
from core.QtModules import (
    pyqtSlot,
    Qt,
    QApplication,
    QDialog,
    QTextEdit,
    QWidget,
)
from .Ui_script import Ui_Dialog


_script = """
from pyslvs import (
    parse_vpoints,
    vpoints_configure,
    data_collecting,
    expr_solving,
)

if __name__ == '__main__':
    vpoints = parse_vpoints("M["\n{0}
        "]")
    exprs = vpoints_configure(vpoints, {1})
    mapping = {{n: 'P{{}}'.format(n) for n in range(len(vpoints))}}
    data_dict, dof = data_collecting(exprs, mapping, vpoints)
    pos = expr_solving(exprs, mapping, vpoints, [0.])
    print(data_dict)
    print("DOF:{{}}".format(dof))
    print(pos)
"""


def slvs_process_script(
    script: Tuple[str],
    inputs: List[Tuple[int, int]]
) -> str:
    """Return parser function script."""
    return _script.format(
        '\n'.join(" " * 8 + '"{}, "'.format(expr) for expr in script),
        inputs
    )


class _ScriptBrowser(QTextEdit):
    
    """Custom text browser to implement text zooming."""
    
    def __init__(self, parent: QWidget):
        super(_ScriptBrowser, self).__init__(parent)
        self.setReadOnly(True)
        self.zoomIn(3)
    
    def wheelEvent(self, event):
        super(_ScriptBrowser, self).wheelEvent(event)
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn(1)
            else:
                self.zoomOut(1)


class ScriptDialog(QDialog, Ui_Dialog):
    
    """Dialog of script preview."""
    
    def __init__(self,
        script: str,
        lexer: RegexLexerMeta,
        filename: str,
        fileformat: List[str],
        parent: QWidget
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
            self.windowFlags() &
            ~Qt.WindowContextHelpButtonHint |
            Qt.WindowMaximizeButtonHint
        )
        self.script_view = _ScriptBrowser(self)
        self.main_layout.insertWidget(1, self.script_view)
        self.code = highlight(script, lexer, HtmlFormatter())
        self.filename = filename
        self.fileformat = fileformat
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.setWindowTitle(self.filename)
        styles = sorted(get_all_styles())
        styles.insert(0, styles.pop(styles.index('default')))
        self.style_option.addItems(styles)
        self.style_option.setCurrentIndex(0)
    
    @pyqtSlot(str, name='on_style_option_currentIndexChanged')
    def __setStyle(self, style: str):
        """Redefind the CSS script of the html."""
        self.script_view.setHtml("<style>{}</style>".format(
            HtmlFormatter(style=get_style_by_name(style))
            .get_style_defs()
        ) + self.code)
    
    @pyqtSlot(name='on_copy_clicked')
    def __copy(self):
        """Copy to clipboard."""
        QApplication.clipboard().setText(self.script_view.toPlainText())
    
    @pyqtSlot(name='on_save_clicked')
    def __save(self):
        """Save to .py file."""
        file_name = self.outputTo(self.filename, self.fileformat)
        if not file_name:
            return
        with open(file_name, 'w', newline = "") as f:
            f.write(self.script_view.toPlainText())
        self.saveReplyBox(self.filename, file_name)
