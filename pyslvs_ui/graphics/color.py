# -*- coding: utf-8 -*-

"""All color options in Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Union
from qtpy.QtCore import QSize
from qtpy.QtGui import QColor, QIcon, QPixmap
from pyslvs import color_names, color_rgb

_Color = Union[str, Tuple[int, int, int], None]


def color_qt(color: _Color) -> QColor:
    """Get color and translate to QColor."""
    if color is None:
        color = "green"
    if isinstance(color, str):
        return QColor(*color_rgb(color))
    else:
        return QColor(*color)


def color_num(color_index: int) -> QColor:
    """Get color by index."""
    return color_qt(color_names[color_index % len(color_names)])


def color_icon(name: _Color, size: int = 20) -> QIcon:
    """Get color block as QIcon by name."""
    color_block = QPixmap(QSize(size, size))
    color_block.fill(color_qt(name))
    return QIcon(color_block)


# Target path color: (line, dot)
_path_color = (
    (color_qt('dark-gray'), color_qt('black')),
    (color_qt('red'), color_qt('dark-red')),
    (color_qt('blue'), color_qt('dark-blue')),
)


def target_path_style(color_index: int) -> Tuple[QColor, QColor]:
    """Get path colors."""
    return _path_color[color_index % len(_path_color)]
